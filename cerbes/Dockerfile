FROM --platform=$BUILDPLATFORM rust:slim-bullseye as builder

WORKDIR /app

ARG TARGETPLATFORM
RUN case "$TARGETPLATFORM" in \
  "linux/arm64") echo aarch64-unknown-linux-gnu > /rust_target.txt ;; \
  "linux/arm/v7") echo armv7-unknown-linux-gnueabihf > /rust_target.txt ;; \
  "linux/amd64") echo x86_64-unknown-linux-gnu > /rust_target.txt ;; \
  *) exit 1 ;; \
esac

RUN apt update && apt install -y libssl-dev pkg-config crossbuild-essential-arm64 crossbuild-essential-armhf && rustup target add $(cat /rust_target.txt)
ENV CARGO_TARGET_ARMV7_UNKNOWN_LINUX_GNUEABIHF_LINKER=/usr/bin/arm-linux-gnueabihf-gcc
ENV CARGO_TARGET_AARCH64_UNKNOWN_LINUX_GNU_LINKER=/usr/bin/aarch64-linux-gnu-gcc

RUN cargo init

COPY ./migration ./migration
COPY ./src ./src
COPY Cargo.toml Cargo.lock .cargo ./

RUN cargo install --path . --target $(cat /rust_target.txt)


FROM debian:bullseye-slim
RUN apt update && apt install -y libssl-dev
COPY ./config ./config
COPY --from=builder /usr/local/cargo/bin/cerbes /usr/local/bin/cerbes
CMD cerbes
