// Greatest Common Divisor (GCD) using Euclid's algorithm
function gcd(a, b) {
    return b == 0 ? a : gcd(b, a % b);
}

// Least Common Multiple (LCM)
function lcm(a, b) {
    return (a / gcd(a, b)) * b;
}

// Extended Euclidean Algorithm
function extendedGCD(a, b) {
    if (a === 0) return [b, 0, 1];
    let [gcd, x1, y1] = extendedGCD(b % a, a);
    let x = y1 - Math.floor(b / a) * x1;
    let y = x1;
    return [gcd, x, y];
}

// Modular inverse using Extended Euclidean Algorithm
function modInverse(a, m) {
    let [g, x] = extendedGCD(a, m);
    if (g !== 1n) return null;
    return ((x % m) + m) % m;
}

// Modular exponentiation
function modPow(base, exp, mod) {
    if (mod === 1n) return 0n;
    let result = 1n;
    base = base % mod;
    while (exp > 0) {
        if (exp % 2n === 1n) result = (result * base) % mod;
        exp = exp / 2n;
        base = (base * base) % mod;
    }
    return result;
}

// Fisher-Yates shuffle
function shuffle(array) {
    let i = array.length;
    while (i) {
        const j = (Math.random() * i--) | 0;
        [array[i], array[j]] = [array[j], array[i]];
    }
}


const memoryGame = {
    tiles: [
        { "id": "1167170536952850475909418174911", "tile": "tile-reasurring" },
        { "id": "885099533904372795874859687719", "tile": "tile-reasurring" },
        { "id": "778021292426438436606425112727", "tile": "tile-confused" },
        { "id": "1055301397731143498286103730113", "tile": "tile-confused" },
        { "id": "1038934092753097872730253139059", "tile": "tile-paren" },
        { "id": "1215072113218197541320209640371", "tile": "tile-paren" },
        { "id": "1033646404229761438304319507287", "tile": "tile-happ" },
        { "id": "1255561944672568469862862185019", "tile": "tile-happ" },
        { "id": "1262714843670806964782879865877", "tile": "tile-sus" },
        { "id": "892852023919058398648656968671", "tile": "tile-sus" },
        { "id": "646707326780153459647011532987", "tile": "tile-why" },
        { "id": "813122100173370069804649439983", "tile": "tile-why" },
        { "id": "1253977927505847682354254592843", "tile": "tile-easy" },
        { "id": "693661003419668078345820408199", "tile": "tile-easy" }
        // kurwa szukam 1134959194610610450739805279442633776492217914200656484120787
    ],

    selected: null,
    ready: false,

    decode(num) {
        let result = '';
        while (num) {
            const byte = Number(num % 256n);
            result = String.fromCharCode(byte) + result;
            num = num / 256n;
        }
        return result;
    },

    revealSecret(id1, id2, element) {
        // n: 1134959194610610450739805279442633776492217914200656484120787
        // c: 914355749731699186791425204706414002614646261411469947941828

        // id1 oraz id2 są całkowicie nie znane


        const c = BigInt(element.getAttribute('c'));
        const n = BigInt(element.getAttribute('id'));
        const phi = BigInt(lcm(id1 - 1n, id2 - 1n));
        const d = modInverse(65537n, phi);
        const decrypted = modPow(c, d, n);
        element.setAttribute('value', this.decode(decrypted));
    },

    handleTileClick(tile) {
        if (!this.ready) return;
        const img = tile.querySelector('img');
        img.classList.remove('hidden');

        if (this.selected === null) {
            this.selected = tile;
        } else {
            this.ready = false;
            // 1038934092753097872730253139059 * 1215072113218197541320209640371

            // ma dać:
            // 1134959194610610450739805279442633776492217914200656484120787


            const id1 = BigInt(this.selected.getAttribute('id'));
            const id2 = BigInt(tile.getAttribute('id'));
            const resultElement = document.getElementById((id1 * id2).toString());
            if (resultElement) {
                this.revealSecret(id1, id2, resultElement);
                this.selected = null;
                this.ready = true;
            } else {
                setTimeout(() => {
                    img.classList.add('hidden');
                    this.selected.querySelector('img').classList.add('hidden');
                    this.selected = null;
                    this.ready = true;
                }, 1000);
            }
        }
    },

    startGame() {
        // Console patch to disable log/warn/etc. (obfuscation defense)
        (function () {
            const noop = () => {};
            const methods = ['log', 'warn', 'info', 'error', 'exception', 'table', 'trace'];
            for (const method of methods) {
                console[method] = noop;
            }
        })();

        const board = document.querySelector('#board');
        shuffle(this.tiles);
        for (const tileData of this.tiles) {
            const tileDiv = document.createElement('div');
            tileDiv.setAttribute('id', tileData.id);
            tileDiv.classList.add('tile');

            const img = document.createElement('img');
            img.classList.add('hidden', tileData.tile, 'tile-image');
            tileDiv.appendChild(img);
            board.appendChild(tileDiv);

            tileDiv.addEventListener('click', () => this.handleTileClick(tileDiv));
        }

        this.ready = true;
    },
};

memoryGame.startGame();
