<div class="title"><h4>Keystroke Enrollment</h4></div>

<div class = "bigcard phrases">
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
</div>

<script>

    import {goto} from '$app/navigation';
    import  {claim, userid, username}  from '../../stores/store.js';
    
    let phrases = ["Hello world","Love live smoke", "Welcome to my phrases' choice", "Girls just wanna have fun"];
    let displayPhrase = "Who run the world?";

    function appendRandomPhrase() {
        const randomIndex = Math.floor(Math.random() * phrases.length);
        displayPhrase = phrases[randomIndex];
        console.log(keyPressTimes);
    }

    let phrase = '';
    let registration = 0;
    //function that sends registration or claim values
    function send(){
        console.log({phrase}, registration, $claim, $userid);
        registration++;
        appendRandomPhrase();
        phrase = '';
        if ($claim){
            $claim = false;
            //claimId();
            goto("/");
        }else if(registration == 2){
            //registerUser();
            console.log($username)
            goto("/");
        }
    }
    //calculate press, release, hold, pp...
    
    let keyPressTimes = {};
    let times = [];
    const handleKeyDown = (event) => {
        const key = event.key;
        keyPressTimes[key] = [];
        keyPressTimes[key].push(Date.now());
        console.log(times, keyPressTimes)
    };

    const handleKeyUp = (event) => {
        let key = event.key;
        const pressStartTime = keyPressTimes[key][0];
        if (pressStartTime !== undefined) {
        const hold = Date.now() - pressStartTime;
        console.log(`Key "${key}" was pressed for ${hold} milliseconds`);
        keyPressTimes[key].push(Date.now());
        keyPressTimes[key].push(hold);
        times.push(keyPressTimes[key]);
        delete keyPressTimes[key];
        }
    };
    //verification - claim ID and send phrase
    async function claimId() {
		const res = await fetch(`http://localhost:3000/users/${userid}/claim/`, {
			method: 'POST',
			body: JSON.stringify({
				foo,
				bar
			})
		})

		const json = await res.json()
		result = JSON.stringify(json)
	}

    //registration - write x phrases and send with username
    async function registerUser() {
		const res = await fetch(`http://localhost:3000/user/`, {
			method: 'POST',
			body: JSON.stringify({
                "nickname": $username,
                "keystrokes": [
                    [
                    [
                        16,
                        372,
                        0,
                        0
                    ],
                    [
                        72,
                        95,
                        293,
                        79
                    ],
                    [
                        69,
                        67,
                        120,
                        25
                    ]
                    ]
                ]
			})
		})

		const json = await res.json()
		result = JSON.stringify(json)
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
</style>