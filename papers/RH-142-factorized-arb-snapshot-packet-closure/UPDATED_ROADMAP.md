# Roadmap after RH-142

The finite frozen binary source-to-projector interface is now closed at all
ten anchors.  The next layer should propagate packet and snapshot balls
through one thresholded update.  It must distinguish:

1. strict threshold margins, where rank/width selection is locally constant;
2. threshold contacts, where no set-valued single branch can be certified;
3. broad but non-swapping coarse projector balls, which may require a
   projector-level update rather than a frame-coordinate Lipschitz bound.

The result remains finite and model-relative; no all-level source theorem is
implied.

