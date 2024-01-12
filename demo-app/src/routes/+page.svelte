
<div class="title"><h4>Keystroke Verification</h4></div>
<div class="bigcard">
  <div class=container>
    <h2><b>Claim Id</b></h2>
  </div>
  <div class="tab1cards">
  {#each { length: 5 } as _,i}
     <div class="container profile" role="" on:click={navigate}> <!--make this clickable-->
      <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
      <div class=container>
        <h4><b>Elena</b></h4>
      </div>
    </div>
  {/each}
  </div>    
  <div class="container">
    <p>or else</p>
    <h3><button class="button" on:click={() => goto("/registration")}>Click to register</button></h3>
  </div>
</div>

<script>
  
  import {goto} from '$app/navigation';
  import { onMount } from 'svelte';
  onMount(async ()=> {
    await loadUsers();
  })
  
  //function that returns the users
  async function loadUsers() {
    const response = await fetch(`http://localhost:3000/users/`); //url api
    const users = await response.json();
    console.log(users)
    return { users };
  } 
  
  
  function navigate(){
    $claim = true
    goto("/insert-phrases")
  }
  import { claim } from '../stores/store.js';

  $: toggle = $claim; // Create a reactive local variable

</script>