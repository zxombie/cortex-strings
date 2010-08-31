#include <string.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include <unistd.h>

#define QUOTEME_(x) #x
#define QUOTEME(x) QUOTEME_(x)

#define NUM_ELEMS(_x) (sizeof(_x) / sizeof((_x)[0]))

#ifndef VERSION
#define VERSION "(unknown version)"
#endif

static const char* version = QUOTEME(VERSION);

/** Current wall time in seconds */
static double now()
{
  struct timespec ts;

  int err = clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
  assert(err == 0);

  return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static int get_arg(int argc, char **argv, int idx, int fallback)
{
  if (argc > idx)
    {
      return atoi(argv[idx]);
    }
  else
    {
      return fallback;
    }
}

static void empty(volatile char *against)
{
  /* We know that there's a 16 k cache with 64 byte lines giving
     a total of 256 lines.  Read randomly from 256*5 places should
     flush everything */
  int offset = (1024 - 256)*1024;

  for (int i = offset; i < offset + 16*1024*3; i += 64)
    {
      against[i];
    }
}

static void xbounce(void *dest, void *src, size_t n)
{
}

static void xmemcpy(void *dest, void *src, size_t n)
{
  memcpy(dest, src, n);
}

static void xmemset(void *dest, void *src, size_t n)
{
  memset(dest, 0, n);
}

static void xstrcpy(void *dest, void *src, size_t n)
{
  strcpy(dest, src);
}

static void xstrlen(void *dest, void *src, size_t n)
{
  (void)strlen(dest);
}

static void xstrcmp(void *dest, void *src, size_t n)
{
  strcmp(dest, src);
}

typedef void (*stub_t)(void *dest, void *src, size_t n);

struct test
{
  const char *name;
  stub_t stub;
};

static const struct test tests[] =
{
  { "memcpy", xmemcpy },
  { "memset", xmemset },
  { "strcpy", xstrcpy },
  { "strlen", xstrlen },
  { "strcmp", xstrcmp },
  { "bounce", xbounce },
  { NULL }
};

static void usage(const char* name)
{
  printf("%s %s: run a string related benchmark.\n"
	 "usage: %s [-c block-size] [-l loop-count] [-f] [-t test-name]\n"
	 , name, version, name);
  exit(-1);
}

int main(int argc, char **argv)
{
  char *src = calloc(1024, 1024);
  char *dest = calloc(1024, 1024);

  assert(src != NULL && dest != NULL);

  srandom(1539);

  for (int i = 0; i < 16*1024; i++)
    {
      src[i] = (char)random() | 1;
      dest[i] = src[i];
    }

  int test_id = get_arg(argc, argv, 1, 0);
  assert(test_id >= 0 && test_id <= NUM_ELEMS(tests));

  int count = 31;
  int loops = 10000000;
  int flush = 0;
  const char *name = NULL;
  int opt;

  while ((opt = getopt(argc, argv, "c:l:ft:hv")) > 0)
    {
      switch (opt)
	{
	case 'c':
	  count = atoi(optarg);
	  break;
	case 'l':
	  loops = atoi(optarg);
	  break;
	case 'f':
	  flush = 1;
	  break;
	case 't':
	  name = strdup(optarg);
	  break;
	case 'h':
	  usage(argv[0]);
	  break;
	default:
	  usage(argv[0]);
	  break;
	}
    }

  const struct test *ptest = NULL;

  if (name == NULL)
    {
      ptest = tests + 0;
    }
  else
    {
      for (const struct test *p = tests; p->name != NULL; p++)
	{
	  if (strcmp(p->name, name) == 0)
	    {
	      ptest = p;
	      break;
	    }
	}
    }

  if (ptest == NULL)
    {
      usage(argv[0]);
    }

  stub_t stub = ptest->stub;

  src[count] = 0;
  dest[count] = 0;

  double start = now();

  for (int i = 0; i < loops; i++)
    {
      (*stub)(dest, src, count);

      if (flush != 0)
	{
	  empty(dest);
	}
    }

  double end = now();
  double elapsed = end - start;

  printf("%s: %s: %.3f for %u loops of %u bytes.  %.3f MB/s\n", QUOTEME(VARIANT), ptest->name, elapsed, loops, count, (double)loops*count/elapsed/(1024*1024));

  return 0;
}
