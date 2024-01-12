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
        />
      </label>
    </form>
    <div>
        <button class="button phrase" on:click={()=>goto("/")}>Register keystrokes</button>
    </div>
</div>
</div>
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



<script>

    //function that sends the phrases (and gets values?)
    import {goto} from '$app/navigation';

    let phrases = ["Hello world","Love live smoke", "Welcome to my phrases' choice", "Ho usato chatGPT"];
    let displayPhrase = "Who run the world?";
    function appendRandomPhrase() {
        const randomIndex = Math.floor(Math.random() * phrases.length);
        displayPhrase = phrases[randomIndex];
    }

</script>