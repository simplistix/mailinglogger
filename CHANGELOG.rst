Changes
=======

.. currentmodule:: mailinglogger

6.0.0 (22 Oct 2022)
-------------------

- Drop Python 2 support.

- Add TLS support.

5.1.0 (8 Sept 2020)
-------------------

- Python 3.8 support.

5.0.0 (30 May 2018)
-------------------

- Python 3 support

- Renaming the modules within the ``mailinglogger`` package to have
  sane capitalisation.

Thanks to Max Shepherd for breaking the back of the Python 3 work.

4.0.0 (26 Jan 2018)
-------------------

- Drop Zope and Plone support

- Drop ZConfig support

- Removed the deprecated ``ignore`` parameter to
  :class:`MailingLogger` and :class:`SummarisingLogger`.
  Use `filter objects`__ instead.

  __ http://docs.python.org/library/logging.html#filter-objects

- Move from ``zope.testrunner`` to `pytest`__ for running tests.

  __ https://docs.pytest.org/en/latest/

- Switch from `manuel`__ to `sybil`__ for checking examples in
  documentation.

  __ http://packages.python.org/manuel/

  __ http://sybil.readthedocs.io/en/latest/

- Moved from buildout to virtualenv for development.

- Gracefully handle bugs elsewhere that call :meth:`SummarisingLogger.close`
  more than once in a multi-threaded or multi-process environment.

3.8.0 (27 Jan 2014)
-------------------

- Implemented flood limiting in :class:`SummarisingLogger` to prevent
  overly large emails being sent.

3.7.0 (18 Jan 2012)
-------------------

- Added the ability to wrap the body of emails sent in a template.

- Added documentation and tools for the sending of HTML emails.

- Fixed a bug that resulted in a unicode error when sending emails
  after a unicode message was logged.

3.6.1 (20 Dec 2011)
-------------------

- Handle the situation where the temporary file used by a
  :class:`SummarisingLogger` is deleted from underneath it.

3.6.0 (24 Nov 2011)
-------------------

- Add support for including messages logged at a lower level in a
  summary email but only triggering the sending of that email when a
  message at a higher level is logged when using
  :ref:`SummarisingLogger <record-and-send-different>`.

3.5.0 (23 Sep 2011)
-------------------

- Add ``X-Log-Level`` header to emails sent. For
  :class:`MailingLogger`, this is the level of the log message being
  emailed. For :class:`SummarisingLogger` this is the highest level of
  any of the messages handled.

3.4.1 (22 Aug 2011)
-------------------

- Fix distribution to include missing files lost through move to Git.

3.4.0 (17 Aug 2011)
-------------------

- Convert documentation to use Sphinx.

- Convert tests to use `testfixures`__ and `manuel`__.

  __ http://packages.python.org/testfixtures/

  __ http://packages.python.org/manuel/

- Drop support for "Zope 3".

3.3.3 (2 Jun 2010)
------------------

- Let the tests also pass in non GMT timezones.

Thanks to Christian Zagrodnick for these changes.

3.3.2 (27 Apr 2010)
-------------------

- Ignores are processed on the interpolated error message.

- Check for empty error messages is done on the interpolated error
  message which in all cases is a string.

Thanks to Christian Zagrodnick for these changes.

3.3.1 (12 Dec 2008)
-------------------
  
- Fix bug that occurred when subject format used %(asctime)s

3.3.0 (11 Dec 2008)
-------------------
  
- Tweak installation documentation

- Add specific test runners for ZConfig, Zope 2 and Zope 3
  support
  
- %(levelname)s in the subject of a SummarisingLogger summary
  is now the highest level message handled by that logger

- Add support for specifying additional headers to the mails
  sent

3.2.2 (4 Nov 2008)
------------------

- Removed hard dependency on ZConfig

- Moved to zc.buildout-based development model

- Fix some doctests for newer versions of zope.testing

3.2.1 (14 Aug 2007)
-------------------

- Fixed egg distribution.

3.2.0 (31 Jul 2007)
-------------------

- Added support for log entry filtering.

Thanks to Jens Vagelpohl for the work which was funded by Campux GmbH.

3.1.0 (18 May 2007)
-------------------

- Added support for SMTP servers that require authentication.

3.0.0 (9 May 2007)
------------------

- Restructured to be used as a python package instead of a Zope
  Product.

- Added comprehensive documentation and tests.

- Added support for use ZConfig.

- Added support for configuration in both Zope 3 and Zope 2.

- Added support for disutils installation and for egg distribution.

2.5.0 (5 Oct 2005)
------------------

- Added compatability for Zope 2.8.x+ at the expense of now
  being incompatible with Zope 2.7.x. 

- Fixed bug in flood protection that often meant no more mail
  was ever sent after midnight on the day when the flood
  protection was triggered.

- Correct X-Mailer header which was set with a trailing newline
  which broke any further headers that were set.

- A date header is now set on all emails sent.

2.4.0 (13 May 2005)
-------------------

- Added sending of X-Mailer header with all emails.

- Added %(hostname)s for use in subject format.

- Fixed bug preventing use of summarising logger introduced in
  2.3.0.

2.3.0 (25 Jan 2005)
-------------------

- Added the ability to limit the number of emails
  sent per hour.

2.2.0 (13 Oct 2004)
-------------------

- Added ability to mute empty log entries

2.1.0 (11 Oct 2004)
-------------------

- Added summarising logger functionality

2.0.1 (1 Aug 2004)
------------------

- Corrected documentation

- Fixed bug that caused the subject to include tracebacks,
  which created a broken mail message.

2.0.0 (28 Jul 2004)
-------------------

- Re-write for Zope 2.7

1.0.1
-----

- Fixed python 1.5 incompatability.

1.0.0
-----

- Initial Release
