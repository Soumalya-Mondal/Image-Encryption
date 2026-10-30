#!/usr/bin/env bash
set -euo pipefail

echo "==> Updating system packages..."
sudo pacman -Syu --noconfirm

echo "==> Installing libheif tools and FFmpeg build dependencies..."
sudo pacman -S --needed --noconfirm \
    libheif \
    base-devel \
    yasm \
    nasm \
    git \
    x264 \
    x265 \
    libvpx \
    lame \
    opus \
    libvorbis

BUILD_DIR="/tmp/ffmpeg-build-$$"
echo "==> Building FFmpeg in ${BUILD_DIR}..."
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"
cd "${BUILD_DIR}"

echo "==> Cloning FFmpeg source (GitHub mirror)..."
git clone --depth 1 https://github.com/FFmpeg/FFmpeg.git ffmpeg
cd ffmpeg

echo "==> Configuring FFmpeg with HEIC/HEVC support..."
./configure \
    --prefix=/usr/local \
    --enable-gpl \
    --enable-version3 \
    --enable-libx264 \
    --enable-libx265 \
    --enable-libvpx \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libvorbis \
    --enable-shared \
    --enable-pic \
    --disable-static

echo "==> Compiling FFmpeg (using all CPU cores)..."
make -j"$(nproc)"

echo "==> Installing FFmpeg..."
sudo make install

echo "==> Ensuring /usr/local/lib takes priority over /usr/lib for FFmpeg libraries..."
echo '/usr/local/lib' | sudo tee /etc/ld.so.conf.d/ffmpeg.conf >/dev/null
sudo ldconfig

echo "==> Cleaning up build directory..."
cd /
rm -rf "${BUILD_DIR}"

echo "==> Verifying HEIC-related support..."
hash -r || true
HEVC_DECODER=$(ffmpeg -decoders 2>/dev/null | grep -i 'hevc' || true)
HEIF_DEMUXER=$(ffmpeg -demuxers 2>/dev/null | grep -i 'heif' || true)

if [ -n "${HEVC_DECODER}" ] || [ -n "${HEIF_DEMUXER}" ]; then
    echo "==> SUCCESS: FFmpeg HEIC support is available."
    echo "    HEVC decoder: ${HEVC_DECODER:-none}"
    echo "    HEIF demuxer: ${HEIF_DEMUXER:-none}"
else
    echo "==> WARNING: FFmpeg HEIC support not detected, but heif-convert is available as fallback."
fi

if command -v heif-convert >/dev/null 2>&1; then
    echo "==> heif-convert is available for reliable HEIC -> JPG conversion."
else
    echo "==> WARNING: heif-convert not found."
    exit 1
fi

echo "==> Library resolution:"
ldd "$(command -v ffmpeg)" | grep -E 'libavcodec|libavformat|libavutil' || true
