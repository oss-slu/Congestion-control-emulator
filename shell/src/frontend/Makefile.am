AM_CPPFLAGS = -I../protobufs -I$(srcdir)/../util -I$(srcdir)/../packet -I$(srcdir)/../http -I$(srcdir)/../httpserver $(XCBPRESENT_CFLAGS) $(XCB_CFLAGS) $(PANGOCAIRO_CFLAGS) $(CXX11_FLAGS)
AM_CXXFLAGS = $(PICKY_CXXFLAGS)

bin_PROGRAMS = mm-link
mm_link_SOURCES = linkshell.cc link_queue.hh link_queue.cc
mm_link_LDADD = -lrt ../util/libutil.a ../packet/libpacket.a $(XCBPRESENT_LIBS) $(XCB_LIBS) $(PANGOCAIRO_LIBS)
mm_link_LDFLAGS = -pthread

bin_PROGRAMS += mm-loss
mm_loss_SOURCES = lossshell.cc loss_queue.hh loss_queue.cc
mm_loss_LDADD = -lrt ../util/libutil.a ../packet/libpacket.a
mm_loss_LDFLAGS = -pthread

bin_PROGRAMS += mm-delay
mm_delay_SOURCES = delayshell.cc delay_queue.hh delay_queue.cc
mm_delay_LDADD = -lrt ../util/libutil.a ../packet/libpacket.a
mm_delay_LDFLAGS = -pthread

lib_LTLIBRARIES = libmod_deepcgi.la
libmod_deepcgi_la_SOURCES = mod_deepcgi.c replayserver_filename.cc
libmod_deepcgi_la_CFLAGS = -I@APACHE2_INCLUDE@ $(libapr1_CFLAGS)
libmod_deepcgi_la_CPPFLAGS = # empty

install-exec-hook:
	
	chown root $(DESTDIR)$(bindir)/mm-link
	chmod u+s $(DESTDIR)$(bindir)/mm-link
	chown root $(DESTDIR)$(bindir)/mm-loss
	chmod u+s $(DESTDIR)$(bindir)/mm-loss
	chown root $(DESTDIR)$(bindir)/mm-delay
	chmod u+s $(DESTDIR)$(bindir)/mm-delay
	
