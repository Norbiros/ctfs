function gcd(a, b) {
    while (b != 0n) {
        [a, b] = [b, a % b];
    }
    return a;
}

function pollardsRho(n) {
    if (n % 2n === 0n) return 2n;
    let x = 2n, y = 2n, d = 1n;
    const f = (x) => (x * x + 1n) % n;

    let iter = 0;
    while (d === 1n) {
        x = f(x);
        y = f(f(y));
        d = gcd((x > y) ? x - y : y - x, n);

        iter++;
        if (iter % 1000 === 0) {
            console.log(`Iter: ${iter}, x: ${x}, y: ${y}, d: ${d}`);
        }
    }
    if (d === n) return null;
    return d;
}


const composite = 1167170536952850475909418174911n;
const factor = pollardsRho(composite);
console.log(factor); // prints a non-trivial factor or null if fails
