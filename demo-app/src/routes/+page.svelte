
{#if visible}
<div class="title"><h4>Keystroke Identification</h4></div>
{/if}
{#if !visible}
<div class="title"><h4>Keystroke Enrollment</h4></div>
{/if}
<div class="bigcard">
  {#if visible}
    <div class=container>
      <h2><b>Claim Id</b></h2>
    </div>
    <div class="tab1cards">
      <div class="container profile">
        <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
        <div class=container>
          <h4><b>Nunzia</b></h4>
        </div>
      </div>
      <div class="container profile">
        <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
        <div class=container>
          <h4><b>Elena</b></h4>
        </div>
      </div>
      <div class="container profile">
        <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
        <div class=container>
          <h4><b>Tommaso</b></h4>
        </div>
      </div>
      <div class="container profile">
        <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
        <div class=container>
          <h4><b>Mary</b></h4>
        </div>
      </div>
    </div>    
    <div class="container">
      <p>or else</p>
      <h3><button class="button" on:click={toggleVisible}>Click to register</button></h3>
    </div>
  {/if}
{#if !visible}

<div class="container margin">
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
  
  <Router>
    <Route path="/insert-phrases"/>
  </Router>
  
  <h3><button class="button" on:click={goToAnotherPage}>Register</button></h3>
</div>
{/if}

</div>
<style>
  .margin{
    padding:15px;
  }
  input{
    margin-bottom: 10px;
    width:100px;
    height:30px;
    font-size: 16px;
  }
</style>


<script>
  //function that returns the users - connect to db
  //function that after click on user, navigate to insert-phrases like below
    //find a way to know if you go to insert-phrases through enrollment or through identification
  let visible = true;

  function toggleVisible() {
    visible = !visible
  }

  import { Router, Link, Route } from 'svelte-routing';  
  import { navigate } from "svelte-routing";
  
  function goToAnotherPage() {
    navigate("/insert-phrases");
        };
        
</script>