const { src, dest, watch } = require("gulp");
const minifyJs = require("gulp-uglify");
const concat = require("gulp-concat");
const babel = require("gulp-babel");

const bundleCore = () => {
  return src("./src/js/core/**/*.js")
    .pipe(concat("core.js"))
    .pipe(
      babel({
        presets: ["@babel/preset-env"],
      })
    )
    .pipe(minifyJs())
    .pipe(dest("./website/static/js/"));
};

const bundleUi = () => {
  return src("./src/js/ui/**/*.js")
    .pipe(
      babel({
        presets: ["@babel/preset-env"],
      })
    )
    .pipe(minifyJs())
    .pipe(dest("./website/static/js/ui/"));
};

const bundleUi_dev = () => {
  return src("./src/js/ui/**/*.js")
    .pipe(
      babel({
        presets: ["@babel/preset-env"],
      })
    )
    .pipe(dest("./website/static/js/ui/"));
};

async function bundleJs() {
  await bundleCore();
  await bundleUi();
}

async function bundleJs_dev() {
  await bundleCore();
  await bundleUi_dev();
}

const devWatch = () => {
  watch("./src/js/**/*.js", bundleJs_dev);
};

exports.default = bundleJs;
exports.watch = devWatch;
exports.dev = bundleUi_dev;
