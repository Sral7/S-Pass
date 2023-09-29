function generatePassword(length, readable, uppercase, lowercase, numbers, symbols, separate, words){
    let password = '';
    if (readable == 3) {
        let extra = '';
        if (numbers) {
        extra += '0123456789'.charAt(Math.floor(Math.random() * 10));
        }
        if (symbols) {
        extra += '!@#$%&*_+-=£€~'.charAt(Math.floor(Math.random() * 17));
        }
        if (length - extra.length > 5 && (numbers || symbols)) {
        let plus = 0;
        if (length > 10) {
            plus = Math.floor(length / 8);
        }
        let extras = Math.floor(Math.random() * (Math.ceil(length / 8) + plus - Math.ceil(length / 16) + 1)) + Math.ceil(length / 16);
        if (numbers && symbols) {
            for (let i = 0; i < extras; i++) {
            extra += '0123456789!@#$%&*_+-=£€~'.charAt(Math.floor(Math.random() * 27));
            }
        } else if (numbers) {
            for (let i = 0; i < extras; i++) {
            extra += '0123456789'.charAt(Math.floor(Math.random() * 10));
            }
        } else if (symbols) {
            for (let i = 0; i < extras; i++) {
            extra += '!@#$%&*_+-=£€~'.charAt(Math.floor(Math.random() * 17));
            }
        }
        }
    

        // Load words from file
        let words = [];
        let request = new XMLHttpRequest();
        request.open('GET', TEXT1_URL, false);
        request.send(null);
        if (request.status === 200) {
        words = request.responseText.split('\n');
        }

        let word_lists = [[], [], [], [], [], []];
        for (let i = 0; i < words.length; i++) {
            word_lists[words[i].length - 1].push(words[i]);
        }

        while (password.length < length - extra.length) {
        let rem;
        if (length - extra.length - password.length < 7) {
            rem = length - extra.length - password.length;
        } else {
            rem = Math.floor(Math.random() * 6) + 1;
        }
        let word = word_lists[rem - 1][Math.floor(Math.random() * word_lists[rem - 1].length)];
        if (uppercase) {
            word = word.charAt(0).toUpperCase() + word.slice(1);
        }
        password += word;
        }

        if (Math.random() < 0.7) {
        password += extra;
        } else {
        password = extra + password;
        }
        if (!lowercase) {
            password = password.toUpperCase();
        }
        console.log(password)
        document.getElementById('output').value = password
        return password;
    }

    if (readable < 3) {
        let chars = '';
        if (uppercase) {
        chars += 'U';
        password += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.charAt(Math.floor(Math.random() * 26));
        }
        if (lowercase) {
        chars += 'L';
        password += 'abcdefghijklmnopqrstuvwxyz'.charAt(Math.floor(Math.random() * 26));
        }
        if (numbers) {
        chars += 'N';
        password += '0123456789'.charAt(Math.floor(Math.random() * 10));
        }
        if (symbols) {
        chars += 'S';
        password += '!@#$%&*_+-=£€~'.charAt(Math.floor(Math.random() * 17));
        }

        for (let i = 0; i < length - chars.length; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
        }

        if (!separate) {
        password = password.split('').sort(function() { return 0.5 - Math.random() }).join('');
        } else {
        if (Math.random() < 0.7) {
            password = password.split('').sort(function(a, b) {
            if (a === 'U' || a === 'L') {
                return -1;
            } else if (b === 'U' || b === 'L') {
                return 1;
            } else if (a === 'N' || a === 'S') {
                return 1;
            } else if (b === 'N' || b === 'S') {
                return -1;
            } else {
                return 0;
            }
            }).join('');
        } else {
            password = password.split('').sort(function(a, b) {
            if (a === 'U' || a === 'L') {
                return 1;
            } else if (b === 'U' || b === 'L') {
                return -1;
            } else if (a === 'N' || a === 'S') {
                return -1;
            } else if (b === 'N' || b === 'S') {
                return 1;
            } else {
                return 0;
            }
            }).join('');
        }
        }

        for (let i = 0; i < password.length; i++) {
        let char = password.charAt(i);
        if (readable === 2) {
            let weights = {'E': 14.7, 'T': 9.1, 'A': 10.2, 'O': 8.5, 'I': 8.0, 'N': 6.7, 'S': 6.3, 'R': 6.0, 'H': 4.1, 'D': 4.3, 'L': 4.0, 'U': 3.2, 'C': 2.8, 'M': 1.4, 'F': 2.2, 'Y': 1.0, 'W': 1.4, 'G': 1.5, 'P': 1.2, 'B': 1.5, 'V': 1.0, 'K': 0.5, 'X': 0.2, 'Q': 0.1, 'J': 0.2, 'Z': 0.1};
            if (char === 'U') {
            password = password.substr(0, i) + r.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', {weights: Object.values(weights)})[0] + password.substr(i + 1);
            } else if (char === 'L') {
            password = password.substr(0, i) + r.choices('abcdefghijklmnopqrstuvwxyz', {weights: Object.values(weights)})[0] + password.substr(i + 1);
            }
        } else if (char === 'U') {
            password = password.substr(0, i) + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.charAt(Math.floor(Math.random() * 26)) + password.substr(i + 1);
        } else if (char === 'L') {
            password = password.substr(0, i) + 'abcdefghijklmnopqrstuvwxyz'.charAt(Math.floor(Math.random() * 26)) + password.substr(i + 1);
        } else if (char === 'N') {
            password = password.substr(0, i) + '0123456789'.charAt(Math.floor(Math.random() * 10)) + password.substr(i + 1);
        } else if (char === 'S') {
            password = password.substr(0, i) + '!@#$%&*_+-=£€~'.charAt(Math.floor(Math.random() * 17)) + password.substr(i + 1);
        }
        }

        document.getElementById('output').value = password
        return password;
    }
    }