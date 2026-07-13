#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using u64 = std::uint64_t;
using i64 = std::int64_t;

bool square_le(u64 a, u64 n) {
    return a == 0 || a <= n / a;
}

bool cube_le(u64 a, u64 n) {
    return a == 0 || a <= n / a / a;
}

struct Options {
    u64 x = 1000000;
    u64 h = 2;
    u64 block_size = 1u << 20;
    unsigned factor_bins = 32;
    std::string theta_text = "0.34,0.38,0.42,0.46,0.49";
    std::string output_prefix = "rough_pair";
};

enum Series : unsigned {
    PS_RIGHT = 0,
    SP_LEFT = 1,
    SS_LEFT = 2,
    SS_RIGHT = 3,
    SERIES_COUNT = 4
};

const char* series_name(Series series) {
    switch (series) {
        case PS_RIGHT: return "PS_right";
        case SP_LEFT: return "SP_left";
        case SS_LEFT: return "SS_left";
        case SS_RIGHT: return "SS_right";
        default: return "unknown";
    }
}

const char* series_cell(Series series) {
    switch (series) {
        case PS_RIGHT: return "PS";
        case SP_LEFT: return "SP";
        case SS_LEFT:
        case SS_RIGHT: return "SS";
        default: return "unknown";
    }
}

const char* series_side(Series series) {
    switch (series) {
        case SP_LEFT:
        case SS_LEFT: return "left";
        case PS_RIGHT:
        case SS_RIGHT: return "right";
        default: return "unknown";
    }
}

struct ThetaStats {
    double theta = 0.0;
    u64 y = 0;
    u64 a = 0;
    u64 n_pp = 0;
    u64 n_ps = 0;
    u64 n_sp = 0;
    u64 n_ss = 0;
    i64 l10 = 0;
    i64 l01 = 0;
    i64 l11 = 0;
    std::vector<u64> factor_hist;

    ThetaStats(double theta_value, u64 cutoff, unsigned bins)
        : theta(theta_value), y(cutoff),
          factor_hist(static_cast<std::size_t>(SERIES_COUNT) * bins, 0) {}

    u64& hist(Series series, unsigned bin, unsigned bins) {
        return factor_hist[static_cast<std::size_t>(series) * bins + bin];
    }
};

struct SegmentFactors {
    std::vector<u64> residual;
    std::vector<u64> spf;
    std::vector<std::uint8_t> omega;

    void resize(std::size_t size) {
        residual.resize(size);
        spf.assign(size, 0);
        omega.assign(size, 0);
    }
};

void print_help(const char* program) {
    std::cout
        << "Usage: " << program << " [options]\n\n"
        << "Exact four-sector diagnostics on starts n in [X,2X).\n"
        << "The shifted value n+h may lie in [2X,2X+h).\n\n"
        << "Options:\n"
        << "  --x N                 Dyadic base X (default 1000000)\n"
        << "  --h N                 Positive even shift (default 2)\n"
        << "  --theta LIST          Comma-separated theta grid\n"
        << "  --block N             Segmented factor-sieve block size\n"
        << "  --factor-bins N       Bins for log(P^-(n))/log(2X+h)\n"
        << "  --output PREFIX       Output file prefix\n"
        << "  --help                Show this message\n\n"
        << "Every cutoff y=floor((2X+h)^theta) must satisfy y^3>2X+h.\n"
        << "This enforces the exact prime/semiprime four-sector regime.\n";
}

u64 parse_u64(const std::string& text, const std::string& name) {
    std::size_t used = 0;
    const unsigned long long value = std::stoull(text, &used);
    if (used != text.size()) {
        throw std::runtime_error("invalid integer for " + name + ": " + text);
    }
    return static_cast<u64>(value);
}

Options parse_options(int argc, char** argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if (arg == "--help") {
            print_help(argv[0]);
            std::exit(0);
        }
        if (i + 1 >= argc) {
            throw std::runtime_error("missing value after " + arg);
        }
        const std::string value = argv[++i];
        if (arg == "--x") options.x = parse_u64(value, arg);
        else if (arg == "--h") options.h = parse_u64(value, arg);
        else if (arg == "--block") options.block_size = parse_u64(value, arg);
        else if (arg == "--factor-bins") {
            const u64 bins = parse_u64(value, arg);
            if (bins > std::numeric_limits<unsigned>::max()) {
                throw std::runtime_error("too many factor bins");
            }
            options.factor_bins = static_cast<unsigned>(bins);
        } else if (arg == "--theta") options.theta_text = value;
        else if (arg == "--output") options.output_prefix = value;
        else throw std::runtime_error("unknown option: " + arg);
    }
    if (options.x < 10) throw std::runtime_error("--x must be at least 10");
    if (options.h == 0 || options.h % 2 != 0) {
        throw std::runtime_error("--h must be a positive even integer");
    }
    if (options.block_size == 0) throw std::runtime_error("--block must be positive");
    if (options.factor_bins == 0) throw std::runtime_error("--factor-bins must be positive");
    if (options.x > static_cast<u64>(std::numeric_limits<i64>::max()) / 4) {
        throw std::runtime_error("--x exceeds the signed Walsh-diagnostic range");
    }
    if (options.block_size > std::numeric_limits<u64>::max() / 10) {
        throw std::runtime_error("--block is too large for progress accounting");
    }
    if (options.x > (std::numeric_limits<u64>::max() - options.h) / 2) {
        throw std::runtime_error("2X+h overflows uint64");
    }
    return options;
}

std::vector<double> parse_thetas(const std::string& text) {
    std::vector<double> values;
    std::stringstream input(text);
    std::string token;
    while (std::getline(input, token, ',')) {
        if (token.empty()) throw std::runtime_error("empty value in --theta list");
        std::size_t used = 0;
        const double theta = std::stod(token, &used);
        if (used != token.size() || !std::isfinite(theta)) {
            throw std::runtime_error("invalid theta: " + token);
        }
        if (!(theta > 1.0 / 3.0 && theta < 0.5)) {
            throw std::runtime_error("theta must lie strictly between 1/3 and 1/2: " + token);
        }
        values.push_back(theta);
    }
    if (values.empty()) throw std::runtime_error("--theta list is empty");
    std::sort(values.begin(), values.end());
    return values;
}

u64 integer_sqrt(u64 n) {
    u64 root = static_cast<u64>(std::sqrt(static_cast<long double>(n)));
    while (square_le(root + 1, n)) ++root;
    while (!square_le(root, n)) --root;
    return root;
}

std::vector<std::uint32_t> primes_up_to(u64 limit_u64) {
    if (limit_u64 > std::numeric_limits<std::uint32_t>::max()) {
        throw std::runtime_error("sqrt(2X+h) exceeds the uint32 prime-table limit");
    }
    const std::size_t limit = static_cast<std::size_t>(limit_u64);
    std::vector<bool> is_prime(limit + 1, true);
    is_prime[0] = false;
    if (limit >= 1) is_prime[1] = false;
    for (std::size_t p = 2; p * p <= limit; ++p) {
        if (!is_prime[p]) continue;
        for (std::size_t multiple = p * p; multiple <= limit; multiple += p) {
            is_prime[multiple] = false;
        }
    }
    std::vector<std::uint32_t> primes;
    for (std::size_t p = 2; p <= limit; ++p) {
        if (is_prime[p]) primes.push_back(static_cast<std::uint32_t>(p));
    }
    return primes;
}

void factor_segment(u64 lo, u64 hi,
                    const std::vector<std::uint32_t>& primes,
                    SegmentFactors& factors) {
    if (hi <= lo) throw std::runtime_error("empty factor segment");
    const u64 length_u64 = hi - lo;
    if (length_u64 > std::numeric_limits<std::size_t>::max()) {
        throw std::runtime_error("factor segment is too large for this platform");
    }
    const std::size_t length = static_cast<std::size_t>(length_u64);
    factors.resize(length);
    for (std::size_t i = 0; i < length; ++i) {
        factors.residual[i] = lo + static_cast<u64>(i);
    }

    const u64 segment_max = hi - 1;
    for (const std::uint32_t p32 : primes) {
        const u64 p = p32;
        if (!square_le(p, segment_max)) break;
        const u64 remainder = lo % p;
        const u64 start = remainder == 0 ? lo : lo + (p - remainder);
        for (u64 value = start; value < hi; value += p) {
            const std::size_t index = static_cast<std::size_t>(value - lo);
            if (factors.residual[index] % p != 0) continue;
            if (factors.spf[index] == 0) factors.spf[index] = p;
            do {
                factors.residual[index] /= p;
                ++factors.omega[index];
            } while (factors.residual[index] % p == 0);
            if (value > std::numeric_limits<u64>::max() - p) break;
        }
    }

    for (std::size_t i = 0; i < length; ++i) {
        if (factors.residual[i] > 1) {
            if (factors.spf[i] == 0) factors.spf[i] = factors.residual[i];
            ++factors.omega[i];
        }
    }
}

unsigned factor_bin(u64 spf, long double log_upper, unsigned bins) {
    const long double alpha = std::log(static_cast<long double>(spf)) / log_upper;
    long double scaled = alpha * static_cast<long double>(bins) / 0.5L;
    if (scaled < 0) scaled = 0;
    unsigned bin = static_cast<unsigned>(scaled);
    if (bin >= bins) bin = bins - 1;
    return bin;
}

void require_signed_range(u64 value, const char* name) {
    if (value > static_cast<u64>(std::numeric_limits<i64>::max())) {
        throw std::runtime_error(std::string(name) + " exceeds int64 diagnostic range");
    }
}

void write_summary(const Options& options, u64 upper,
                   const std::vector<ThetaStats>& stats,
                   double elapsed_seconds) {
    const std::string path = options.output_prefix + "_summary.csv";
    std::ofstream output(path);
    if (!output) throw std::runtime_error("cannot open output file: " + path);
    output << "x,start,stop_exclusive,h,shifted_upper_exclusive,theta,y,"
              "block_size,factor_bins,A,N_PP,N_PS,N_SP,N_SS,R,"
              "L10,L01,L11,inversion_numerator,inverted_N_PP,"
              "inversion_error,sector_sum_error,elapsed_seconds\n";
    output << std::setprecision(17);
    for (const ThetaStats& row : stats) {
        require_signed_range(row.a, "A");
        require_signed_range(row.n_pp, "N_PP");
        const i64 a = static_cast<i64>(row.a);
        const i64 numerator = a - row.l10 - row.l01 + row.l11;
        const i64 inverted = numerator / 4;
        const i64 inversion_error = inverted - static_cast<i64>(row.n_pp);
        const i64 sector_sum = static_cast<i64>(row.n_pp + row.n_ps + row.n_sp + row.n_ss);
        const i64 sector_error = sector_sum - a;
        output
            << options.x << ',' << options.x << ',' << 2 * options.x << ','
            << options.h << ',' << upper << ',' << row.theta << ',' << row.y << ','
            << options.block_size << ',' << options.factor_bins << ','
            << row.a << ',' << row.n_pp << ',' << row.n_ps << ','
            << row.n_sp << ',' << row.n_ss << ',' << (row.a - row.n_pp) << ','
            << row.l10 << ',' << row.l01 << ',' << row.l11 << ','
            << numerator << ',' << inverted << ',' << inversion_error << ','
            << sector_error << ',' << elapsed_seconds << '\n';
    }
    std::cout << "wrote " << path << '\n';
}

void write_factor_bins(const Options& options, u64 upper,
                       const std::vector<ThetaStats>& stats) {
    const std::string path = options.output_prefix + "_factor_bins.csv";
    std::ofstream output(path);
    if (!output) throw std::runtime_error("cannot open output file: " + path);
    output << "x,h,shifted_upper_exclusive,theta,y,series,cell,side,"
              "bin_index,alpha_lo,alpha_hi,count\n";
    output << std::setprecision(17);
    for (const ThetaStats& row : stats) {
        for (unsigned series_index = 0; series_index < SERIES_COUNT; ++series_index) {
            const Series series = static_cast<Series>(series_index);
            for (unsigned bin = 0; bin < options.factor_bins; ++bin) {
                const double alpha_lo = 0.5 * static_cast<double>(bin) /
                                        static_cast<double>(options.factor_bins);
                const double alpha_hi = 0.5 * static_cast<double>(bin + 1) /
                                        static_cast<double>(options.factor_bins);
                output
                    << options.x << ',' << options.h << ',' << upper << ','
                    << row.theta << ',' << row.y << ',' << series_name(series) << ','
                    << series_cell(series) << ',' << series_side(series) << ','
                    << bin << ',' << alpha_lo << ',' << alpha_hi << ','
                    << row.factor_hist[static_cast<std::size_t>(series_index) *
                                            options.factor_bins + bin]
                    << '\n';
            }
        }
    }
    std::cout << "wrote " << path << '\n';
}

}  // namespace

int main(int argc, char** argv) {
    try {
        const Options options = parse_options(argc, argv);
        const u64 upper = 2 * options.x + options.h;
        const std::vector<double> theta_values = parse_thetas(options.theta_text);

        std::vector<ThetaStats> stats;
        for (const double theta : theta_values) {
            const long double raw = std::pow(static_cast<long double>(upper),
                                             static_cast<long double>(theta));
            if (!(raw >= 2 && raw < static_cast<long double>(std::numeric_limits<u64>::max()))) {
                throw std::runtime_error("cutoff y is outside uint64 range");
            }
            const u64 y = static_cast<u64>(std::floor(raw));
            if (cube_le(y, upper)) {
                std::ostringstream message;
                message << "floor((2X+h)^theta)^3 <= 2X+h for theta=" << theta
                        << "; increase X or theta";
                throw std::runtime_error(message.str());
            }
            stats.emplace_back(theta, y, options.factor_bins);
        }

        const u64 prime_limit = integer_sqrt(upper - 1);
        std::cerr << "generating primes through " << prime_limit << "...\n";
        const std::vector<std::uint32_t> primes = primes_up_to(prime_limit);
        std::cerr << "base primes: " << primes.size() << '\n';

        const long double log_upper = std::log(static_cast<long double>(upper));
        SegmentFactors factors;
        const auto started = std::chrono::steady_clock::now();
        u64 processed = 0;

        for (u64 lo = options.x; lo < 2 * options.x;) {
            const u64 remaining = 2 * options.x - lo;
            const u64 starts_in_block = std::min(options.block_size, remaining);
            const u64 hi = lo + starts_in_block;
            const u64 extended_hi = hi + options.h;
            factor_segment(lo, extended_hi, primes, factors);

            for (u64 offset = 0; offset < starts_in_block; ++offset) {
                const std::size_t left = static_cast<std::size_t>(offset);
                const std::size_t right = static_cast<std::size_t>(offset + options.h);
                const u64 pair_spf = std::min(factors.spf[left], factors.spf[right]);
                const auto first_rejected = std::lower_bound(
                    stats.begin(), stats.end(), pair_spf,
                    [](const ThetaStats& row, u64 spf) { return row.y < spf; });
                const std::size_t candidate_cutoffs =
                    static_cast<std::size_t>(first_rejected - stats.begin());
                if (candidate_cutoffs == 0) continue;

                const unsigned omega_left = factors.omega[left];
                const unsigned omega_right = factors.omega[right];
                if ((omega_left != 1 && omega_left != 2) ||
                    (omega_right != 1 && omega_right != 2)) {
                    throw std::runtime_error(
                        "four-sector invariant failed despite y^3>2X+h");
                }
                const bool left_prime = omega_left == 1;
                const bool right_prime = omega_right == 1;
                const int lambda_left = left_prime ? -1 : 1;
                const int lambda_right = right_prime ? -1 : 1;
                const unsigned left_bin = left_prime ? 0 :
                    factor_bin(factors.spf[left], log_upper, options.factor_bins);
                const unsigned right_bin = right_prime ? 0 :
                    factor_bin(factors.spf[right], log_upper, options.factor_bins);

                for (std::size_t index = 0; index < candidate_cutoffs; ++index) {
                    ThetaStats& row = stats[index];
                    ++row.a;
                    row.l10 += lambda_left;
                    row.l01 += lambda_right;
                    row.l11 += lambda_left * lambda_right;
                    if (left_prime && right_prime) {
                        ++row.n_pp;
                    } else if (left_prime) {
                        ++row.n_ps;
                        ++row.hist(PS_RIGHT, right_bin, options.factor_bins);
                    } else if (right_prime) {
                        ++row.n_sp;
                        ++row.hist(SP_LEFT, left_bin, options.factor_bins);
                    } else {
                        ++row.n_ss;
                        ++row.hist(SS_LEFT, left_bin, options.factor_bins);
                        ++row.hist(SS_RIGHT, right_bin, options.factor_bins);
                    }
                }
            }

            processed += starts_in_block;
            lo = hi;
            if (processed == options.x || processed % (10 * options.block_size) == 0) {
                std::cerr << "processed " << processed << " / " << options.x << " starts\n";
            }
        }

        const auto finished = std::chrono::steady_clock::now();
        const double elapsed = std::chrono::duration<double>(finished - started).count();
        write_summary(options, upper, stats, elapsed);
        write_factor_bins(options, upper, stats);

        for (const ThetaStats& row : stats) {
            const i64 inverted =
                (static_cast<i64>(row.a) - row.l10 - row.l01 + row.l11) / 4;
            if (inverted != static_cast<i64>(row.n_pp) ||
                row.a != row.n_pp + row.n_ps + row.n_sp + row.n_ss) {
                throw std::runtime_error("post-run exact identity check failed");
            }
        }
        std::cout << "exact four-sector and Liouville inversion checks passed\n";
        std::cout << "elapsed_seconds=" << std::setprecision(6) << elapsed << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << '\n';
        return 1;
    }
}
