<div class="title"><h4>Keystroke Enrollment</h4></div>
<div class = "bigcard phrases">
{#if !claimingDone}
<div class="container phrases">
    <div class="container phrase">
        {#if displayPhrase}
        <h2>{displayPhrase}</h2>
        {/if}
    </div>
    <button class="button phrase" on:click={appendRandomPhrase}>reload</button>
    <form>
      <label>
        <input class="phrasebox"
          required
          type="text"
          placeholder="Write the phrase that appears on top here"
          bind:value={phrase}
          on:keydown={handleKeyDown}
          on:keyup={handleKeyUp}
        />
      </label>
    </form>
    <div>
        <button class="button phrase" on:click={send}>Register keystrokes</button>
    </div>
</div>
{:else}
<div class="container phrases">
    <div>
        <h2 class="result">Your result is: {result.likelihood}</h2>
        <h2 class="result">whith a score of: {result.prediction}</h2>
    </div>
    <div>
        <button class="button phrase" on:click={()=>goto("/")}>Go back home</button>
    </div>
</div>
{/if}
</div>

<script>

    import {goto} from '$app/navigation';
    import  {claim, userid, username}  from '../../stores/store.js';
    
    let phrases = ["The pen is on the table", "I will be with you in a moment", "Welcome to my phrases' choice", "Think before you speak", "It's raining cats and dogs",
                    "Veni Vidi Vici", "Work in progress", "I'm feeling blue today", "To shoot to a little mouse with a cannon", "Walking on sunshine", "A cat has nine lives"];
    let displayPhrase = "Hello world";
    let claimingDone = false;
    let result = "";

    //function that load another phrase to write
    function appendRandomPhrase() {
        const randomIndex = Math.floor(Math.random() * phrases.length);
        displayPhrase = phrases[randomIndex];
        console.log(keyPressTimes);
    }

    let phrase = '';
    let registration = 0;
    let claiming = 0;
    let keystrokes = [];

    //function that sends registration or claim values
    function send(){
        console.log({phrase}, registration, $claim, $userid);
        registration++;
        claiming ++;
        let phrase_key = [];
        for(let i = 1; i<times.length; i++)
        {
            phrase_key.push(calculateParams(times[i-1],times[i]));
        }
        keystrokes.push(phrase_key);
        keyPressTimes = {};
        times = [];
        appendRandomPhrase();
        phrase = '';
        if ($claim){
            if(claiming == 3)
            {
                $claim = false;
                claimId();
                console.log($username)
                claimingDone = true;
            }
            
        }else if(registration == 5){
            registerUser();
            console.log(keystrokes);
            console.log($username)
            goto("/");
        }
    }
    
    //register press, release and hold time
    let keyPressTimes = {};
    let times = [[0,0,0,0]];

    const handleKeyDown = (event) => {
        const key = event.key;
        let code = event.which;
        console.log(key);
        if(code=="219")code = 191;
        console.log(code);
        keyPressTimes[key] = [];
        keyPressTimes[key].push(code);
        keyPressTimes[key].push(Date.now());
        console.log(times, keyPressTimes)
    };

    const handleKeyUp = (event) => {
        let key = event.key;
        const pressStartTime = keyPressTimes[key][1];
        if (pressStartTime !== undefined) {
        const hold = Date.now() - pressStartTime;
        console.log(`Key "${key}" was pressed for ${hold} milliseconds`);
        keyPressTimes[key].push(Date.now());
        keyPressTimes[key].push(hold);
        times.push(keyPressTimes[key]);
        delete keyPressTimes[key];
        }
    };

    //calculate values for evaluation
    function calculateParams(i, j){
       
        let h = Number(j[3]);
        let pp = Number(j[1]-i[1]);
        let rp = Number(j[1]-i[2]);
        //If considering first keystroke
        if(pp>1000){pp=0;rp=0;}
        return [Number(j[0]), Math.round(h), Math.round(pp), Math.round(rp)]
    }

    //verification - claim ID and send phrase
    async function claimId() {
		const res = await fetch(`http://localhost:3000/users/${$userid}/claim/`, {
			method: 'POST',
			body: JSON.stringify(keystrokes)
		})

		const json = await res.json();
        result = JSON.stringify(json);
        console.log(result)
		result = JSON.parse(result);
	}

    //registration - write x phrases and send with username
    async function registerUser() {
		const res = await fetch(`http://localhost:3000/user/`, {
			method: 'POST',
			body: JSON.stringify({
                "nickname": $username,
                "keystrokes": [keystrokes]
			})
		})

		const json = await res.json();
		result = JSON.stringify(json);

	}

</script>

<style>
    
    .bigcard.phrases{
        margin-right: 25%;
        margin-left: 25%;
    }
    
    input {
        width: 500px;
        float: left;
        height: 35px;
        line-height: 3em;
        font-size:14pt;
        border-radius: 5px;
        border: 2px solid #4A7C59;
        margin-bottom:15px;
    }
    .button.phrase{
        border-radius: 25px;
        background-color:#8FC0A9;
        color: rgb(0, 0, 0);
        padding: 15px 15px;
        text-align: center;
        display: inline-block;
        font-size: 20px;
        border: none;
        margin-bottom: 20px;
        font-weight: bold;
    }
    
    .container{
        margin: 20px auto;
    }
    
    .phrase{
        border: 2px solid #4A7C59;
        border-radius: 25px;
        background-color: white;
        
    }
    h2{
        font-weight: normal;
    }

    .result{
        margin-bottom:20px;
    }
</style>