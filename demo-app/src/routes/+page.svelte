<h1>Hello World</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<div
    class="card"
    >
    <h5 class="mt-5 text-4xl text-green-500 dark:text-purple-500">Accedi</h5>

    <form
      class="flex grow flex-col justify-evenly"
    >
      <label class="flex flex-col justify-around">
        <div class="text-md dark:text-white">Email</div>
        <input
          required
          class="w-4/6 self-center rounded border-[1px] border-graphite p-1 text-sm"
          type="text"
          placeholder="@"
          v-model="email"
        />
      </label>
      <label class="flex flex-col">
        <div class="text-md dark:text-white">Password</div>
        <input
          required
          class="w-4/6 self-center rounded border-[1px] border-graphite p-1 text-sm"
          type="password"
          placeholder="Password"
          v-model="password"
        />
      </label>
    </form>
  </div>