FROM --platform=$BUILDPLATFORM rust:slim-bullseye as builder

WORKDIR /app

RUN apt update && apt install -y libssl-dev pkg-config

RUN cargo init

COPY ./migration ./migration
COPY ./src ./src
COPY Cargo.toml Cargo.lock ./

RUN cargo install --path . 


FROM debian:bullseye-slim
RUN apt update && apt install libssl-dev
COPY ./config ./config
COPY --from=builder /usr/local/cargo/bin/* /usr/local/bin
CMD cerbes