# Changelog

## [2.3.0](https://github.com/juliloa/DevOps_Back/compare/v2.2.0...v2.3.0) (2025-05-11)


### Features

* Complete user system: authentication, password reset, user creation/edit/delete, and Tailwind CSS forms. ([#24](https://github.com/juliloa/DevOps_Back/issues/24)) ([fef2de2](https://github.com/juliloa/DevOps_Back/commit/fef2de24c810f89cbf3b58edb39dbc4965404025))


### Bug Fixes

* mark unused request parameter with _ ([79bb34c](https://github.com/juliloa/DevOps_Back/commit/79bb34c64bf2b40134a0d65e602688da12f41bd5))

## [2.2.0](https://github.com/juliloa/DevOps_Back/compare/v2.1.1...v2.2.0) (2025-05-11)


### Features

* improve movement UI and enhance JWT middleware ([#22](https://github.com/juliloa/DevOps_Back/issues/22)) ([69fb07b](https://github.com/juliloa/DevOps_Back/commit/69fb07b467e91867e6844d414fd251c2f0640369))

## [2.1.1](https://github.com/juliloa/DevOps_Back/compare/v2.1.0...v2.1.1) (2025-05-02)


### Bug Fixes

* Added [@require](https://github.com/require)_http_methods decorator to restrict login_view to GET and POST methods only ([#18](https://github.com/juliloa/DevOps_Back/issues/18)) ([08493e1](https://github.com/juliloa/DevOps_Back/commit/08493e1adda2e2b20e67ae6a5d0bd0830dd76107))
* **login:** organize and enforce GET and POST usage in login views ([#20](https://github.com/juliloa/DevOps_Back/issues/20)) ([6174500](https://github.com/juliloa/DevOps_Back/commit/6174500d1c2881acf1ec8afb0ddd8840124b1438))
* Removed dependency on external scripts and added integrity to CDN resources ([50fea56](https://github.com/juliloa/DevOps_Back/commit/50fea5651c09132363892e5e841712710a0906a3))
* silence unused request param warning in root_redirect view ([9538580](https://github.com/juliloa/DevOps_Back/commit/9538580a4a5320dea5c8a7cca2bb5301802aea81))

## [2.1.0](https://github.com/juliloa/DevOps_Back/compare/v2.0.3...v2.1.0) (2025-04-20)


### Features

* Module Warehouses into Main ([#15](https://github.com/juliloa/DevOps_Back/issues/15)) ([0538017](https://github.com/juliloa/DevOps_Back/commit/0538017c147556397690f65205e399016d2b7359))


### Bug Fixes

* Update attribute_filter.py ([68a33da](https://github.com/juliloa/DevOps_Back/commit/68a33dac212732d031ea955b1c9e8ecb1bb51637))

## [2.0.3](https://github.com/juliloa/DevOps_Back/compare/v2.0.2...v2.0.3) (2025-04-15)


### Bug Fixes

* Added # NOSONAR to ignore the unnecessary parameter warning ([77f0a5b](https://github.com/juliloa/DevOps_Back/commit/77f0a5bd8d8f0f51d94a9392226e7e7d7db38ad1))

## [2.0.2](https://github.com/juliloa/DevOps_Back/compare/v2.0.1...v2.0.2) (2025-04-15)


### Bug Fixes

* Update views.py ([5f3101d](https://github.com/juliloa/DevOps_Back/commit/5f3101d1b0fc7952937ead989fdac97b9db6ef90))

## [2.0.1](https://github.com/juliloa/DevOps_Back/compare/v2.0.0...v2.0.1) (2025-04-13)


### Bug Fixes

* stop tracking cache files, LogiVag.sql and move SECRET_KEY to .env ([#10](https://github.com/juliloa/DevOps_Back/issues/10)) ([a7ad95b](https://github.com/juliloa/DevOps_Back/commit/a7ad95bb7def205be23f54a37dbc1cc62da18655))

## [2.0.0](https://github.com/juliloa/DevOps_Back/compare/v1.0.1...v2.0.0) (2025-04-05)


### ⚠ BREAKING CHANGES

* add user authentication using JWT ([#7](https://github.com/juliloa/DevOps_Back/issues/7))

### Features

* add user authentication using JWT ([#7](https://github.com/juliloa/DevOps_Back/issues/7)) ([a126f8a](https://github.com/juliloa/DevOps_Back/commit/a126f8a8954bc8c75fbb57517cdedbca7615b9cf))

## [1.0.1](https://github.com/juliloa/DevOps_Back/compare/v1.0.0...v1.0.1) (2025-04-02)


### Bug Fixes

* Update release-please.yml ([cbba2ca](https://github.com/juliloa/DevOps_Back/commit/cbba2caa8703e8354bacd764e0f886970eda26e8))

## 1.0.0 (2025-04-02)


### ⚠ BREAKING CHANGES

* Configure database models, relationships, and set up GitHub Actions release workflow ([#4](https://github.com/juliloa/DevOps_Back/issues/4))

### Features

* add initial database schema with tables and triggers ([#3](https://github.com/juliloa/DevOps_Back/issues/3)) ([83a5c55](https://github.com/juliloa/DevOps_Back/commit/83a5c55a2331527a598c810fbc5c1740703a3da1))
* Add name in README ([#1](https://github.com/juliloa/DevOps_Back/issues/1)) ([e9beab9](https://github.com/juliloa/DevOps_Back/commit/e9beab9a82f2f45a6d3549082257362f3e7c32ce))
* Configure database models, relationships, and set up GitHub Actions release workflow ([#4](https://github.com/juliloa/DevOps_Back/issues/4)) ([bac5732](https://github.com/juliloa/DevOps_Back/commit/bac5732e20aee502dc8c3146fdd7e4b21db981e1))
