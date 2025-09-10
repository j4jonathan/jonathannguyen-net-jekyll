---
layout: page
title: Jonathan Nguyen
id: home
permalink: /
---

I'm the founder & CEO of [Unsensible](https://www.unsensible.com). 

Herein lies esoterica and arbitrary code—use at your own risk!

For articulate thoughts, connect with me on [LinkedIn](https://www.linkedin.com/in/jonathannguyen)

Deep discourse with APAC founders—[podcast](https://www.unsensible.com/podcast).

If you need to get in touch—[gesticulate wildly](https://bsky.app/profile/jonathannguyen.net).

![Team America Signal]({{ '/assets/images/TheSignal_TeamAmerica.gif' | relative_url }})

*Hoc opus numquam perfectum*

---

<strong>Recently updated notes</strong>

<ul>
  {% assign recent_notes = site.notes | sort: "last_modified_at_timestamp" | reverse %}
  {% for note in recent_notes limit: 5 %}
    <li>
      {{ note.last_modified_at | date: "%Y-%m-%d" }} — <a class="internal-link" href="{{ site.baseurl }}{{ note.url }}">{{ note.title }}</a>
    </li>
  {% endfor %}
</ul>

<style>
  .wrapper {
    max-width: 46em;
  }
</style>