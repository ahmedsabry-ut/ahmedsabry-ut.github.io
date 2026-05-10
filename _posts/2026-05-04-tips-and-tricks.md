---
title: "Tips and Tricks"
date: 2026-05-04
---

Now that the degree is behind me, I wanted to take a step back and write down the tips and tricks that helped me streamline my work and get through the program while juggling full-time work and life. Some of these I figured out early on, others took a few semesters of trial and error. Hopefully a future student finds something here useful.

## Separate Email and Chrome Profile

UT Austin actually gives you separate Gmail and Outlook accounts to work with - I'm not quite sure if this is still the case, I noticed a few email changes, but regardless, I was able to set up a separate Chrome profile and have all school related work in its isolated window. Having that separation helps isolate your studies from your life and it's a bit more organized this way, so a very greatly under-appreciated perk.

## GitHub

With this new email, you can set up your own school GitHub account (or maybe the school sets it up for you, I forgot) and then have all your own school related code under that account, which is great!

I would generally, create a repository for each class, and then push my work there. It's so important to have Git just because of the trial and error process of trying to get the results that you want. This skill of saving your work will be especially apparent when you get to the machine learning classes that involve trying different model weights/architectures etc.

Speaking of GitHub, I wanted to share how I was able to "switch" between my different user profiles when committing code. The last thing you need is some "permissions denied" error when you accidentally try to push code to your school's GitHub using your personal account and vice versa. Here's the configuration I used in my `.gitconfig` file:

```ini
...
[includeIf "gitdir:~/<path to personal code folder>/personal/**"]
  path = ~/<path to personal code folder>/personal/.gitconfig
[includeIf "gitdir:~/<path to school code folder>/UT-Austin/**"]
  path = ~/<path to school code folder>/UT-Austin/.gitconfig
...
```

So under each folder, both personal and school, there's a `.gitconfig` with that account's specific details, but under the root `.gitconfig`, it points to which profile to use based on the folder I'm under.

## Other Websites


### MSDS Hub

I was very lucky to find out about the [MSDS Hub](https://msdshub.com/) website early on. This website is just for students to review classes and it helped me decide which classes I can take based on the kind of workload I was willing to take on in the semester. If we use the 1-10 Scale, I would generally first sort on the difficulty first, and then aim to take a combined workload of ~13-18 hours.

I would generally spend the majority of my time before registration on this website and I'd try to gauge what my next 4 months would look like without classes and then choosing when I've come to terms with how much time I'd have to spend outside of work to focus on my classes.

### Ed Discussion

This was the discussion board website that all MSDS courses used. I also find it to be extremely underrated. Every now and then you'll get a helpful tip for how to complete an assignment question, or even find out that the final was optional. This website helped facilitate communication in a way that I don't think Canvas could reasonably offer.

## Planning the Program of Work

I'd generally recommend the same approach I took, which is just to gauge how many sort of major events are coming up/how much mental energy you have/general interest in courses/other students' reviews to help decide how much workload you're willing to take on. A general rule of thumb is:

| Available Time to Spare per week | Number of Courses |
| -------------------------------- | :---------------: |
| 5 - 10                           |         1         |
| 11 - 20                          |         2         |
| 20+                              |         3         |

Don't do 4+. I'm pretty confident you even need permission to do 3, I never tried it though. Not all courses are created equal, some easier, some harder, but you'll adapt regardless.

## Study and Note-Taking Workflow

Get an iPad and install the Notability app. Take notes as you watch lectures. Some classes let you take your notes to exams, so you could print them all later and it's eco-friendly. Some professors have their own lecture module PDF files which is also great - I'd recommend taking notes down as they explain instead of just printing completed notes - the learning is in the process, not the final result.

## Assignments and Exams

Start assignments early, and don't spend more than 2 hours on them at a time. Finish them over the course of like 10 days. Tackling the entire assignment on in 1 go is bound to do your head in. Start with the easy problems first. Get that quick easy dopamine to help you get through the rest of the assignment. And this is also where Notability comes in again because each new question can get its own page and you can sort your answers later.

## Looking Back

If I could tell myself something on day one, it would be that the degree is less about any single course and more about building a system you can sustain for years. A separate browser profile, a school Git setup, and an honest look at your calendar before you register are not glamorous, but they save you from a thousand small frictions that add up when you are already tired from work.

I would also say: be kind to yourself about the pace. I took some combinations that were harder than they needed to be because I was in a hurry to finish, and I learned the hard way that one extra rough semester does not get you to the finish line faster if you are burned out. The program is long enough that small habits matter more than heroics—starting assignments early, using Ed when you are stuck, and picking a workload you can actually carry based on real reviews, not just optimism.

You will adapt either way. The courses are not all the same difficulty, and life will throw surprises your way. What helped me most was treating school like a serious second job: protected time, version-controlled work, and a community of other students who had already taken the class. Stick with that, and you will get through it.
