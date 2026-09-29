# stremthru-ad-buddy

[StremThru](https://github.com/MunifTanjim/stremthru) buddy that finds which torrents are cached on AllDebrid.

AllDebrid removed `magnet/instant`, so this service uploads the magnets, reads `ready`, then deletes what it added. Magnets already in your library are never deleted, and your key is never sent to a third party.

## Usage

```yaml
services:
  stremthru:
    image: muniftanjim/stremthru:latest
    environment:
      - STREMTHRU_BUDDY_URI=http://stremthru-ad-buddy:8080

  stremthru-ad-buddy:
    build: .
    environment:
      - ALLDEBRID_KEY=${ALLDEBRID_KEY}
      - HTTPS_PROXY=http://proxy:8888  # optional, if AllDebrid blocks your IP
```
