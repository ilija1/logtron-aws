<template>
  <div>
    <nav
      class="navbar header has-shadow is-primary"
      role="navigation"
      aria-label="main navigation"
    >
      <div class="navbar-brand">
        <a class="navbar-item" href="/"> Logtron-AWS Documentation </a>

        <div class="navbar-burger">
          <span />
          <span />
          <span />
        </div>
      </div>
    </nav>

    <section class="main-content columns">
      <aside class="column is-2 section">
        <template v-for="(section, section_key) of sections">
          <p :key="section_key" class="menu-label is-hidden-touch">
            {{ section.name }}
          </p>
          <ul :key="section_key" class="menu-list">
            <li
              v-for="(item, key) of section.items"
              :key="`${section_key}_${key}`"
            >
              <nuxt-link :to="item.to" exact-active-class="is-active">
                <b-icon :icon="item.icon" /> {{ item.title }}
              </nuxt-link>
            </li>
          </ul>
        </template>
        <p class="menu-label is-hidden-touch">Source Code</p>
        <ul class="menu-list">
          <li>
            <a href="https://github.com/ilija1/logtron-aws" target="_blank">
              <b-icon icon="github" /> Github
            </a>
          </li>
        </ul>
      </aside>

      <div class="container column is-10">
        <nuxt />
      </div>
    </section>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sections: [
        {
          name: 'General',
          items: [
            {
              title: 'Home',
              icon: 'home',
              to: { name: 'index' },
            },
            {
              title: 'Getting Started',
              icon: 'school',
              to: { name: 'content-slug', params: { slug: 'getting-started' } },
            },
          ],
        },
        {
          name: 'Reference',
          items: [
            {
              title: 'API Reference',
              icon: 'book-open-outline',
              to: { name: 'content-slug', params: { slug: 'api-reference' } },
            },
            {
              title: 'Configuration',
              icon: 'tools',
              to: { name: 'content-slug', params: { slug: 'configuration' } },
            },
          ],
        },
      ],
    }
  },
}
</script>
