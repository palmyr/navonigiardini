var gulp = require('gulp');
var sass = require('gulp-sass');
var concat = require('gulp-concat');

gulp.task('scss', function(){
    return gulp.src('./scss/import.scss')
        .pipe(sass())
        .pipe(concat('./style.css'))
        .pipe(gulp.dest('docs/css'))
});

gulp.task('watch', function(){
    gulp.watch('./scss/**/*.scss', gulp.series('scss'));
});

gulp.task('build', gulp.series('scss'));