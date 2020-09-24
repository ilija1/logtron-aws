<template>
  <section class="section">
    <article class="content">
      <h1 class="title">{{ page.title }}</h1>

      <hr />
      <h2 class="subtitle is-6 toc">Table of Contents</h2>
      <ul class="toc">
        <li
          v-for="link of page.toc"
          :key="link.id"
          :class="{ toc2: link.depth === 2, toc3: link.depth === 3 }"
        >
          <NuxtLink :to="`#${link.id}`">{{ link.text }}</NuxtLink>
        </li>
      </ul>
      <hr />

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
  async asyncData({ $content, params }) {
    const page = await $content(params.slug).fetch()

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
