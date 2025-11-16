# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased


## [0.4.1] - 2025-11-25
### Changed
  * `API._request`: the `endpoint` is now optional. When not provided (default), the base URL will be used
  * `urljoin` is now used to combine base URL and endpoint

### Added
  * Python 3.13 and 3.14 officially supported

### Fixed
  * `pip-audit` vulnerability issues. Updated dependencies (minor)


## [0.4.0] - 2025-06-08
### Changed
  * Make response headers public. **Warning**: backwards incompatible change
  * `FakeHTTPClient`: don't append None values to the history. **Warning**: backwards incompatible change

### Added
  * `data` parameter for `HTTPClient.request` to send form or raw data
  * `status_code` for the `HTTPError` exception
  * Tests for the query params


## [0.3.0] - 2024-10-17
### Added
  * Support for HTTP timeouts


## [0.2.0] - 2024-10-02
### Fixed
  * `HTTPResponse.ok` is now a property as was planned originally

### Added
  * `http.HTTPError` exception
  * `HTTPResponse.raise_for_status` method
  * `API.__str__` method

### Changed
  * Split `http.base` module into separate modules like `response.py` and `errors.py`
  * HTTP exceptions are now importable as `http.errors`


## [0.1.3] - 2024-10-02
### Added
  * `http.auth` module. Support for Basic auth
  * `params` argument for the `HTTPClient.request` to simplify query parameters usage
  * `cert` argument for the `HTTPClient.request` to allow client side certificates


## [0.1.2] - 2024-09-20
### Added
  * `http.fake_client` module


## [0.1.1] - 2024-09-18
### Added
  * `http.requests_client` module


## [0.1.0] - 2024-09-17
### Added
  * Initial version
