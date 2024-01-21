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
    
        {#if isLoading}
        <h2>Loading...</h2>
        {:else}
            {#if result.likelihood !== undefined}
                <!-- Display your API response data here -->
                <h2 class="result">Your result is: {result.prediction}</h2>
                <h2 class="result">whith a score of: {result.likelihood}</h2>
            {:else}
            <h2>No data available.</h2>
            {/if}
        {/if}
    <div>
        <button class="button phrase" on:click={()=>goto("/")}>Go back home</button>
    </div>
</div>
{/if}
</div>

<script>

    import {goto} from '$app/navigation';
    import  {claim, userid, username}  from '../../stores/store.js';
    
    let phrases = [
        "Will you and KB be around this afternoon?",
        "The others raise their eyebrows.",
        "Through this account cash flows to corporate.",
        "I'm waiting until she comes home.",
        "This year I can walk and it's so much better.",
        "We can discuss options early next week.",
        "I am really not wanting to come back.",
        "Ava, do we need to worry about this?",
        "Throw it away and not let it touch your heart.",
        "Others voting against represented the defense ministry.",
        "That would be a fitting memorial to those who died.",
        "If lunch doesn't work then how about coffee?",
        "We don't recommend McNair this week as a result.",
        "If it needs to be paid, we will need to add the day to the deal.",
        "Emerson Fittipaldi has never had an engine this good.",
        "I'll take up my problem with weak Scott H.",
        "The buses will be identified by their cities of origin.",
        "Sources said the officers will be part of the coordination office.",
        "A report Thursday showed wholesale prices fell 0.1 percent in April.",
        "But there have been so many changes in plans that I'm not surprised.",
        "Also, it appears no payment is required tomorrow.",
        "Juppe described Emile Jonassaint as a puppet with no legitimacy.",
        "Tricia needs to know if she needs to invoice them or not.",
        "We are proceeding with a great reception so far."
    ]
;
    let displayPhrase = "To shoot a little mouse with a cannon.";
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
        console.log(times)
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
    let isLoading = true;
    //verification - claim ID and send phrase
    async function claimId() {
		try{
           
            const res = await fetch(`http://localhost:3000/users/${$userid}/claim/`, {
			method: 'POST',
			body: JSON.stringify(keystrokes)
            })
            isLoading = false
            const json = await res.json()
            result = JSON.stringify(json)
            result = JSON.parse(result)
        }catch(error){
            console.error('Error fetching data:', error);
            isLoading = false;
        }
	}

    //registration - write x phrases and send with username
    async function registerUser() {
		const res = await fetch(`http://localhost:3000/user/`, {
			method: 'POST',
			body: JSON.stringify({
                "nickname": $username,
                "keystrokes": keystrokes
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