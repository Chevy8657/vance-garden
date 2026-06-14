#!/bin/bash

set -e

PACKAGE_NAME="vance_garden_mvp"
STAMP=$(date +"%Y%m%d_%H%M%S")
OUTDIR="dist_${STAMP}"

mkdir -p "$OUTDIR/$PACKAGE_NAME"

cp app.py "$OUTDIR/$PACKAGE_NAME/"
cp vance_engine.py "$OUTDIR/$PACKAGE_NAME/"
cp requirements.txt "$OUTDIR/$PACKAGE_NAME/"
cp Procfile "$OUTDIR/$PACKAGE_NAME/" 2>/dev/null || true
cp runtime.txt "$OUTDIR/$PACKAGE_NAME/" 2>/dev/null || true
cp README.md "$OUTDIR/$PACKAGE_NAME/"
cp -r templates "$OUTDIR/$PACKAGE_NAME/"
cp -r contacts "$OUTDIR/$PACKAGE_NAME/" 2>/dev/null || true
cp -r launch_package "$OUTDIR/$PACKAGE_NAME/" 2>/dev/null || true

cd "$OUTDIR"
zip -r "${PACKAGE_NAME}_${STAMP}.zip" "$PACKAGE_NAME"

echo "PACKAGE CREATED:"
echo "$OUTDIR/${PACKAGE_NAME}_${STAMP}.zip"
