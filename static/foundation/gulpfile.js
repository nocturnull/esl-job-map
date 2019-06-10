var gulp          = require('gulp');
var webpack = require('webpack-stream');
var minify = require('gulp-minify');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var $             = require('gulp-load-plugins')();
var autoprefixer  = require('autoprefixer');

var sassPaths = [
    'node_modules/foundation-sites/scss',
    'node_modules/motion-ui/src'
];

function sass() {
    return gulp.src('scss/app.scss')
        .pipe($.sass({
            includePaths: sassPaths,
            outputStyle: 'compressed' // if css compressed **file size**
        })
            .on('error', $.sass.logError))
        .pipe($.postcss([
            autoprefixer({ browsers: ['last 2 versions', 'ie >= 9'] })
        ]))
        .pipe(rename('app.min.css'))
        .pipe(gulp.dest('dist/'));
}

function vendorJs() {
    return gulp.src([
        'node_modules/jquery/dist/jquery.js',
        'node_modules/what-input/dist/what-input.js',
        'node_modules/foundation-sites/dist/js/foundation.js'
    ])
        .pipe(minify({
            noSource: true
        }))
        .pipe(concat('vendor.min.js'))
        .pipe(gulp.dest('dist/'));
}

function siteJs() {
    return gulp.src('js/app.js')
        .pipe(webpack({
            output: {
                filename: 'app.min.js'
            },
            mode: 'production'
        }))
        .pipe(gulp.dest('dist/'));
}

function watch() {
    gulp.watch("scss/*.scss", sass);
}

gulp.task('sass', sass);
gulp.task('vendor-js', vendorJs);
gulp.task('site-js', siteJs);
gulp.task('default', gulp.parallel(['sass', 'vendor-js', 'site-js'], watch));
