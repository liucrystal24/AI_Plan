globalThis.a = 10;
var fn = "globalThis.a = globalThis.a+1;console.log(globalThis.a)"
var runner = new Function(fn)
runner()
console.log(globalThis.a)