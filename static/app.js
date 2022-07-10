class BoggleGame {

    constructor(boardId, secs = 60) {
        this.secs = secs;
        this.showTimer();

        this.board = $('#' + boardId);
        this.score = 0;
        this.words = new Set();

        // this.timer = setInterval(this.tick.bind(this), 1000);

        $("#guess", this.board).on("submit", this.submitWord.bind(this));
    }

    showWord(word) {
        // shows the words already guessed
        $('#words', this.board).append(`<li>${word}</li>`);
    }

    showScore() {
        // show the game score
        $(".score", this.board).text(this.score);
    }

    showMessage(msg, cls) {
        // shows the message after you submit a word
        $("#msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }


    async submitWord(evt) {
        evt.preventDefault();
        //select the button with the id of guess on the board
        const $word = $('#word', this.board);
        //get the value of the guess
        let word = $word.val();
        //return if there's no value
        if (!word) return;

        //if the set already has the word/it's been guessed throw an error
        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`, "err");
            return;
        }
        //send the word to the server to check if it's valid
        const resp = await axios.get("/check-word", { params: { word: word } });
        if (resp.data.result === 'not-word') {
            this.showMessage(`${word} is not a valid word`, "err");
        } else if (resp.data.result === "not-on-board") {
            this.showMessage(`${word} is not a word on this board`, "err");
        } else {
            //appends the guess to the list of words
            this.showWord(word);
            //adds word length to the score
            this.score += word.length;
            //updates the score
            this.showScore();
            //adds word to the set of words guessed
            this.words.add(word);
            //shows a message that the word was added
            this.showMessage(`Added: ${word}`, "ok");
        }

        //empty the submission field
        $word.val('').focus();
    }

    //update the timer
    showTimer() {
        $(".timer", this.board).text(this.secs);
    }

    //handles a second passing down
    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.endGame();
        }
    }

    async endGame() {
        $("#guess", this.board).hide();
        const resp = await axios.post("/post-score", { score: this.score });
        if (resp.data.brokeRecord) {
            this.showMessage(`New record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Final Score: ${this.score}`, "ok");
        }
    }
}

