# Project Roadmap

## Tasks

- [ ] Scraping test-set images with a python MediaWiki API for immediate color-indexing by a KD-Tree.
  - [ ] Craft API requests for the smallest image resolutions available.
  - [ ] Use PIL / Pillow to identify the primary image color, and its percent prevalence in the image.
  - [ ] Setup KD-Tree RGB colorspace index (3-D KD-Tree) to store color indexing results and image metadata.
- [ ] Ranking
  - [ ] Use color distance from searched color value and color prevalence to rank results.
- [ ] Searching
  - [ ] Create search frontend which fetches matching metadata as text
	- [ ] Color wheel for color selection
	- [ ] Threshold control for color search.
	- [ ] MediaWiki metadata filtering / search (boolean text queries).
	- [ ] Display images fetched from Wikimedia in full resolution.
	- [ ] Color picker for refinement searches from loaded image results
