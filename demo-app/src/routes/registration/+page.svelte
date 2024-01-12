<div class="title"><h4>Keystroke Enrollment</h4></div>
<div class="bigcard registration">
  <div class="container"> 
    
    <form>
      <label>
        <h2 class="margin">Please choose a username to be identified</h2>
        <input
          required
          type="text"
          placeholder="user123"
          v-model="username"
        />
      </label>
    </form>
    
    <h3>
      <button class="button" on:click={()=>goto("/insert-phrases")}>Register</button>
      <button class="button" on:click={()=>goto("/")}>Go Back</button>
    </h3>
  </div>
  </div>
  <script>
    import {goto} from '$app/navigation';
  </script>

  <style>
    .bigcard.registration{
      margin-right: 20%;
      margin-left: 20%;
	}

  input{
		margin-bottom: 10px;
		width:100px;
		height:30px;
		font-size: 16px;
	}
  </style>

