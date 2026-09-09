"""Hard-coded local filesystem paths used by tests that need to read/write files on disk.

Note these are absolute paths specific to one checkout (`git_folder`), not portable config; see
`utils/README.md` for context.
"""

git_folder = "/home/milchior/generate-musical-image"
"""Absolute path to this repository's checkout root, as found on the machine these tests were written on."""

test_folder = f"{git_folder}/test_files"
"""Folder holding fixture files used by tests."""

out_folder = f"{test_folder}/generated"
"""Scratch folder tests write generated output to."""
