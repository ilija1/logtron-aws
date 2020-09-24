<template>
  <section class="section">
    <article class="content">
      <nuxt-content :document="page" />
    </article>
    <hr />
    <div class="field">
      <b-tag rounded>Last updated {{ formatDate(page.updatedAt) }}</b-tag>
    </div>
  </section>
</template>

<script>
export default {
  async asyncData({ $content }) {
    const page = await $content('home').fetch()

    return {
      page,
    }
  },
  methods: {
    formatDate(date) {
      return new Date(date).toLocaleString('en')
    },
  },
}
</script>
