bin_PROGRAMS = freeplay_trainer

freeplay_trainer_SOURCES = src/freeplay_trainer.cc
freeplay_trainer_LDADD = -lrcsc_agent -lrcsc_geom -lrcsc_param -lrcsc_rcg \
	-lrcsc_net -lrcsc_gz -lrcsc_ann -lrcsc_time

AM_CXXFLAGS = -I. -D_GNU_SOURCE -D_XOPEN_SOURCE=600 -Wall -Wextra -std=gnu++11
