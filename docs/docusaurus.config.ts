import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'PyMUSAS',
  tagline: 'PYthon Multilingual Ucrel Semantic Analysis System',
  favicon: '/pymusas/img/favicon.png',
  staticDirectories: ['static'],

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://ucrel.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/pymusas/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'ucrel', // Usually your GitHub org/user name.
  projectName: 'pymusas', // Usually your repo name.

  onBrokenLinks: 'throw',
  trailingSlash: false,

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/ucrel/pymusas/edit/main/docs/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
          routeBasePath: '/',
        },
        /*blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },*/
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    // Cannot be a SVG.
    image: '/pymusas/img/ucrel_logo.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'PyMUSAS',
      logo: {
        alt: 'UCREL logo',
        src: '/pymusas/img/ucrel_logo.png',
      },
      items: [
        {
          type: 'doc',
          docId: 'usage/getting_started/intro',
          position: 'left',
          label: 'Usage',
        },
        {to: '/api/base', label: 'API', position: 'left'},
        //{to: '/blog', label: 'Blog', position: 'left'},
        {
          href: 'https://github.com/ucrel/pymusas',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Usage',
              to: '/',
            },
            {
              label: 'API',
              to: '/api/base',
            },
            
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Bluesky',
              href: 'https://bsky.app/profile/ucrelnlp.bsky.social',
            },
            {
              label: 'YouTube',
              href: 'https://www.youtube.com/@ucrelcrs8222',
            },
          ],
        },
        {
          title: 'More',
          items: [
            /*{
              label: 'Blog',
              to: '/blog',
            },*/
            {
              label: 'GitHub',
              href: 'https://github.com/ucrel/pymusas',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} UCREL. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
