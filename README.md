IBL OpenBadges XBlock v1
=============

This is the XBlock (an extension component for the Open edX course platform) to allow awarding digital badges from an online course using Open edX. 

####Warning: This XBlock implemented badge awarding using the Achievery service (via their API), which has been discontinued. The XBlock is thus no longer in working order.

The Open Badges XBlock was developed by [IBL Studios](http://iblstudios.com/), with conceptual and feature design by [Lorena A. Barba](http://lorenabarba.com/) and Michael Amigot, and used in Prof. Barba's open online course ["Practical Numerical Methods with Python."](http://openedx.seas.gwu.edu/courses/GW/MAE6286/2014_fall/about) It went live in the course on December 2014.

General consultancy on the principles for open digital badges in education was provided by [Prof. Daniel T. Hickey](http://remediatingassessment.blogspot.com/) and his team at Indiana University. The badges were awarded using the service of the [Achievery](http://achievery.com/) platform. 

## Summary of features

1. The badges can be awarded from a **"Graded Sub-section"** in a course in Open edX. The instructor sets the minimum score for eligibility for the badge, and configures the badge component with the data of the badge service, badge id, custom messages for the user, etc.
2. Once added to a Graded Sub-section, the open-badges XBlock will automatically check a user's score for that sub-section when the user enters the sub-section.
3. While the user does not have enough score for eligibility, the XBlock will display a custom message indicating this.
4. Once the user has enough score, the XBlock will reveal the badge image and the input fields to claim the badge.
5. The user fills the claim form, entering URL fields for their learning evidence and others.
6. Once awarded, the badge is privately available in the user's account on the badge service. The user then "claims" the badge to make it public. (This is the normal operation of open-badge services.)

###See how it works:

To see how the open-badges XBlock works, from the instructor's point of view, see this screencast:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=QNAgxQu1OYw
" target="_blank"><img src="http://img.youtube.com/vi/QNAgxQu1OYw/0.jpg" 
alt="IBL badges XBlock demo" width="240" height="180" border="10" /></a>


---

_Note: Remember to setup the badge with the variable `debug_mode` set to 1,
this will activate the application debug mode. If debug mode is ON you'll be able to 
award the same badge many times for the same user. Under production mode, remember
to turn off the `debug_mode` variable._

---

###Presented at:
**Open edX Conference**, Cambridge, MA (November 2014)
See the [slides of the presentation](http://dx.doi.org/10.6084/m9.figshare.1252211), released under CC-BY on the Figshare repository.
