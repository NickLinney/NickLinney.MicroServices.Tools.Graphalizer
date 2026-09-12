FROM debian:13-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132 AS runtime

ARG PLANTUML_VERSION=1.2026.8
ARG PLANTUML_SHA256=5e1ecfa8ecd32c90b03bbf3b1eb6f020943f98ab0fcf4032be31a0002ee2c462
ARG MERMAID_CLI_VERSION=11.16.0
ARG PUPPETEER_VERSION=24.31.0

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/graphalizer/src \
    PLANTUML_JAR=/opt/plantuml/plantuml.jar \
    PLANTUML_SECURITY_PROFILE=SECURE \
    PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    HOME=/tmp/graphalizer-home \
    XDG_CACHE_HOME=/tmp/graphalizer-cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        chromium \
        curl \
        default-jre-headless \
        fontconfig \
        fonts-dejavu-core \
        fonts-liberation \
        graphviz \
        librsvg2-bin \
        nodejs \
        npm \
        python3-minimal \
        time \
        tini \
    && mkdir -p /opt/plantuml /opt/graphalizer /tmp/graphalizer-home /tmp/graphalizer-cache \
    && curl --fail --location --silent --show-error \
        "https://github.com/plantuml/plantuml/releases/download/v${PLANTUML_VERSION}/plantuml-${PLANTUML_VERSION}.jar" \
        --output /opt/plantuml/plantuml.jar \
    && echo "${PLANTUML_SHA256}  /opt/plantuml/plantuml.jar" | sha256sum --check --strict \
    && npm install --global --omit=dev \
        "@mermaid-js/mermaid-cli@${MERMAID_CLI_VERSION}" \
        "puppeteer@${PUPPETEER_VERSION}" \
    && npm cache clean --force \
    && apt-get purge -y --auto-remove curl npm \
    && rm -rf /var/lib/apt/lists/* /root/.npm \
    && groupadd --gid 10001 graphalizer \
    && useradd --uid 10001 --gid graphalizer --no-create-home --shell /usr/sbin/nologin graphalizer \
    && chown -R graphalizer:graphalizer /tmp/graphalizer-home /tmp/graphalizer-cache

COPY --chown=root:root docker/puppeteer-config.json /opt/graphalizer/puppeteer-config.json
COPY --chown=root:root src /opt/graphalizer/src

WORKDIR /opt/graphalizer
USER 10001:10001

ENTRYPOINT ["/usr/bin/tini", "--", "python3", "-m", "graphalizer"]
CMD ["--help"]

FROM runtime AS test
COPY --chown=root:root tests /opt/graphalizer/tests
ENV GRAPHALIZER_INTEGRATION=1
ENTRYPOINT ["/usr/bin/tini", "--", "python3"]
CMD ["-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"]
