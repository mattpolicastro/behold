# Bundled models

## spot.obj

"Spot" by [Keenan Crane](https://www.cs.cmu.edu/~kmcrane/Projects/ModelRepository/),
from his 3D Model Repository. Triangulated tessellation, 2930 vertices / 5856
triangles.

**Public domain.** Crane's repository is released under a
[CC0 1.0 Universal Public Domain Dedication][cc0], and the archive's own README
(kept here verbatim as `spot.README.txt`) states:

> As the sole author of this data, I hereby release it into the public domain.

[cc0]: https://creativecommons.org/publicdomain/zero/1.0/

Included so `gyre` has something to render out of the box. Nothing else in this
repository depends on it — delete it and everything still works.

### Why not the Utah teapot?

The obvious choice, but its licensing is genuinely unresolved: Martin Newell's
original dataset carries no explicit grant, CC0 has been *suggested* but never
confirmed, Apache has [a LEGAL ticket][asf] open about it, and
`common-3d-test-models` records its license as, literally, "missing". Spot is
unambiguous, so Spot it is.

[asf]: https://issues.apache.org/jira/browse/LEGAL-525
