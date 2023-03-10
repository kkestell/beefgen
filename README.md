# BeefGen

BeefGen uses the [Clang AST](https://clang.llvm.org/docs/IntroductionToTheClangAST.html) to automatically generate [Beef](https://www.beeflang.org/) bindings from C headers.

**BeefGen is a work in progress and full of bugs. This probably isn't the repository you're looking for.**

## Dependencies

BeefGen uses `clang`, so make sure it's installed.

```console
$ sudo pacman -Sy clang
```

The [lark](https://github.com/lark-parser/lark) parsing toolkit is used to parse C declarations. Make sure it's installed:

```console
$ pip install -r requirements.txt
```

## License

BeefGen uses the [Unlicense](LICENSE).
