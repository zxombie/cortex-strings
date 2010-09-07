/** A simple harness that times how long a string function takes to
 * run.
 */

/* PENDING: Add EPL */

#include <string.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include <unistd.h>

#define NUM_ELEMS(_x) (sizeof(_x) / sizeof((_x)[0]))

#ifndef VERSION
#define VERSION "(unknown version)"
#endif

/** Make sure a function is called by using the return value */
#define SPOIL(_x)  volatile int x = (int)(_x); (void)x

/** Type of functions that can be tested */
typedef void (*stub_t)(void *dest, void *src, size_t n);

/** Meta data about one test */
struct test
{
  /** Test name */
  const char *name;
  /** Function to test */
  stub_t stub;
};

/** Flush the cache by reading a chunk of memory */
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

/** Stub that does nothing.  Used for calibrating */
static void xbounce(void *dest, void *src, size_t n)
{
  SPOIL(0);
}

/** Stub that calls memcpy */
static void xmemcpy(void *dest, void *src, size_t n)
{
  SPOIL(memcpy(dest, src, n));
}

/** Stub that calls memset */
static void xmemset(void *dest, void *src, size_t n)
{
  SPOIL(memset(dest, 0, n));
}

/** Stub that calls strcpy */
static void xstrcpy(void *dest, void *src, size_t n)
{
  SPOIL(strcpy(dest, src));
}

/** Stub that calls strlen */
static void xstrlen(void *dest, void *src, size_t n)
{
  SPOIL(strlen(dest));
}

/** Stub that calls strcmp */
static void xstrcmp(void *dest, void *src, size_t n)
{
  SPOIL(strcmp(dest, src));
}

/** All functions that can be tested */
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

/** Show basic usage */
static void usage(const char* name)
{
  printf("%s %s: run a string related benchmark.\n"
         "usage: %s [-c block-size] [-l loop-count] [-f] [-t test-name]\n"
         , name, VERSION, name);

  printf("Tests:");

  for (const struct test *ptest = tests; ptest->name != NULL; ptest++)
    {
      printf(" %s", ptest->name);
    }

  printf("\n");

  exit(-1);
}

/** Find the test by name */
static const struct test *find_test(const char *name)
{
  if (name == NULL)
    {
      return tests + 0;
    }
  else
    {
      for (const struct test *p = tests; p->name != NULL; p++)
	{
          if (strcmp(p->name, name) == 0)
	    {
              return p;
	    }
	}
    }

  return NULL;
}

/** Setup and run a test */
int main(int argc, char **argv)
{
  /* Buffers to read and write from */
  char *src = calloc(1024, 1024);
  char *dest = calloc(1024, 1024);

  assert(src != NULL && dest != NULL);

  /* Fill the first 16 k with non-zero, reproducable random data */
  srandom(1539);

  for (int i = 0; i < 16*1024; i++)
    {
      src[i] = (char)random() | 1;
      dest[i] = src[i];
    }

  /* Number of bytes per call */
  int count = 31;
  /* Number of times to run */
  int loops = 10000000;
  /* True to flush the cache each time */
  int flush = 0;
  /* Name of the test */
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

  /* Find the test by name */
  const struct test *ptest = find_test(name);

  if (ptest == NULL)
    {
      usage(argv[0]);
    }

  /* Make sure the buffers are null terminated for any string tests */
  src[count] = 0;
  dest[count] = 0;

  struct timespec start, end;
  int err = clock_gettime(CLOCK_MONOTONIC, &start);
  assert(err == 0);

  /* Preload */
  stub_t stub = ptest->stub;

  for (int i = 0; i < loops; i++)
    {
      (*stub)(dest, src, count);

      if (flush != 0)
	{
          empty(dest);
	}
    }

  err = clock_gettime(CLOCK_MONOTONIC, &end);
  assert(err == 0);

  /* Pull the variant name out of the executable */
  char *variant = strrchr(argv[0], '-');

  if (variant == NULL)
    {
      variant = argv[0];
    }

  double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) * 1e-9;

  /* Dump both machine and human readable versions */
  printf("%s:%s:%u:%u:%.6f: took %.6f s for %u calls to %s of %u bytes.  ~%.3f MB/s\n", 
         variant + 1, ptest->name, count, loops, elapsed,
         elapsed, loops, ptest->name, count,
         (double)loops*count/elapsed/(1024*1024));

  return 0;
}
