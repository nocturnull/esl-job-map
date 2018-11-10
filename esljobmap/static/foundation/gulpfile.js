var gulp = require('gulp');
var webpack = require('webpack-stream');
var minify = require('gulp-minify');
var rename = require('gulp-rename');
var concat = require('gulp-concat');
var $    = require('gulp-load-plugins')();

var sassPaths = [
  'node_modules/foundation-sites/scss',
  'node_modules/motion-ui/src'
];

gulp.task('sass', function() {
  return gulp.src('scss/app.scss')
    .pipe($.sass({
      includePaths: sassPaths,
      outputStyle: 'compressed' // if css compressed **file size**
    })
      .on('error', $.sass.logError))
    .pipe($.autoprefixer({
      browsers: ['last 2 versions', 'ie >= 9']
    }))
    .pipe(rename('app.min.css'))
    .pipe(gulp.dest('dist/'));
});

gulp.task('vendor-js', function () {
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

});

gulp.task('site-js', function () {
    return gulp.src('js/app.js')
        .pipe(webpack({
            output: {
                filename: 'app.min.js'
            },
            mode: 'production'
        }))
        .pipe(gulp.dest('dist/'));
});

gulp.task('default', ['sass', 'vendor-js', 'site-js'], function() {
  gulp.watch(['scss/**/*.scss'], ['sass']);
});
