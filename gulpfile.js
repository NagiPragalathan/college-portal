const { src, dest, watch } = require('gulp');
const minifyJs = require("gulp-uglify");
const concat = require("gulp-concat");
const babel = require("gulp-babel");

const bundleCore = () => {
    return src("./src/js/core/**/*.js")
    .pipe(concat('core.js'))
    .pipe(babel({
        presets: ["@babel/preset-env"]
        }))
    .pipe(minifyJs())
    .pipe(dest("./website/static/js/"));
}

const bundleUi = () => {
    return src("./src/js/ui/**/*.js")
    .pipe(babel({
        presets: ["@babel/preset-env"]
        }))
    .pipe(minifyJs())
    .pipe(dest("./website/static/js/ui/"));
}

async function bundleJs () {
    await bundleCore();
    await bundleUi();
}

const devWatch = () => {
    watch("./src/js/**/*.js", bundleJs);
}

exports.default = bundleJs;
exports.watch = devWatch;
