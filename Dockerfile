# 1. Install dependencies only when needed
FROM node:18-alpine AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN apk add --no-cache libc6-compat
WORKDIR /app
# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \
    if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
    elif [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then yarn global add pnpm && pnpm i; \
    else echo "Lockfile not found." && exit 1; \
    fi

# 2. Rebuild the source code only when needed
FROM node:18-alpine AS builder
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN rm -rf .*.local
RUN rm -rf .env.*.local
# This will do the trick, use the corresponding env file for each environment.
# COPY docker/prod/.env.prod .env.production
RUN cd ./frontend && yarn build

# 3. Production image, copy all the files and run next
# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM imcapsule/capsulehub-ml-repo:reward-pts-api-base_v1.1
# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app
ENV NODE_ENV=production

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .
COPY --from=deps --chown=wagtail:wagtail /app/node_modules ./node_modules
COPY --from=builder --chown=wagtail:wagtail /app/frontend/build ./frontend/build
# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn rewards_backend.wsgi:application
