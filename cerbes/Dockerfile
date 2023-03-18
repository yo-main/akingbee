FROM --platform=$BUILDPLATFORM rust:slim-bullseye as builder

ARG TARGET="x86_64-unknown-linux-gnu"
ARG BUILDPLATFORM="linux/amd64"
WORKDIR /app

RUN apt update && apt install -y libssl-dev pkg-config crossbuild-essential-arm64 crossbuild-essential-armhf && rustup target add $TARGET
ENV CARGO_TARGET_ARMV7_UNKNOWN_LINUX_GNUEABIHF_LINKER=/usr/bin/arm-linux-gnueabihf-gcc

RUN cargo init

COPY ./migration ./migration
COPY ./src ./src
COPY Cargo.toml Cargo.lock .cargo ./

RUN cargo install --path . --target $TARGET


FROM debian:bullseye-slim
RUN apt update && apt install libssl-dev
COPY ./config ./config
COPY --from=builder /usr/local/cargo/bin/cerbes /usr/local/bin/cerbes
CMD cerbes