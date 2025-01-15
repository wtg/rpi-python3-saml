For some reason, NextAuth does not like it when we use wellKnown component because RPI redirects to another URl. Therefore, we need to set all the URL's manually.

Inside settings.ts, you will find the options that you should pass into the NextAuth object. In addition, you will need to request the secret values from DOTCIO, and open a ticket to do so.

In addition, I used a JWT strategy, but if you want to use a database session strategy, that would be fine also, the documentation would be there.