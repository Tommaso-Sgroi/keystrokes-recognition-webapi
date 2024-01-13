<div class="title"><h4>Keystroke Enrollment</h4></div>
<div class="bigcard registration">
  <div class="container"> 
    <form on:submit|preventDefault={handleSubmit}>
      <label>
        <h2 class="margin" id="name">Please choose a username to be identified</h2>
        <input
          required
          type="text"
          placeholder="user123"
          v-model="username"
          bind:value={$username}
        />
      </label>
      <h3><button class="button" type="submit">Register</button>
      <button class="button" on:click={()=>goto("/")}>Go Back</button>
    </h3>
    </form>
    
  </div>
  </div>
  <script>
    import {goto} from '$app/navigation';
    import {username} from '../../stores/store.js';
    
    function handleSubmit(){
      if ($username.trim() !== "") {
        goto("/insert-phrases");
      } else {
        alert("Please enter a value.");
      }
    }
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

