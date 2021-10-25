// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'PyMUSAS',
  tagline: 'PYthon Multilingual Ucrel Semantic Analysis System',
  url: 'https://ucrel.github.io',
  baseUrl: '/pymusas/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/favicon.png',
  organizationName: 'ucrel', // Usually your GitHub org/user name.
  projectName: 'pymusas', // Usually your repo name.
  trailingSlash: false,

  presets: [
    [
      '@docusaurus/preset-classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl: 'https://github.com/ucrel/pymusas/edit/main/docs/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
          routeBasePath: '/',
        },
        /*blog: {
          showReadingTime: true,
          // Please change this to your repo.
          editUrl:
            'https://github.com/facebook/docusaurus/edit/main/website/blog/',
        },*/
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'PyMUSAS',
        logo: {
          alt: 'UCREL logo',
          src: 'img/ucrel_logo.svg',
        },
        items: [
          {
            type: 'doc',
            docId: 'documentation/intro',
            position: 'left',
            label: 'Documentation',
          },
          {to: '/api/file_utils', label: 'API', position: 'left'},
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
            title: 'Docs',
            items: [
              {
                label: 'Documentation',
                to: '/',
              },
              {
                label: 'API',
                to: '/api/file_utils',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Twitter',
                href: 'https://twitter.com/UCREL_NLP',
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
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
