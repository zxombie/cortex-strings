#include <string.h>
#include <sys/time.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

static double now()
{
  struct timeval tv;

  gettimeofday(&tv, NULL);

  return tv.tv_sec + tv.tv_usec * 1e-6;
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

static void __attribute__((noinline)) xmemcpy(char *dest, char *src, size_t n)
{
  memcpy(dest, src, n);
}

static void __attribute__((noinline)) xstrcpy(char *dest, char *src)
{
  strcpy(dest, src);
}

static void __attribute__((noinline)) xmemset(void *dest, int c, size_t n)
{
  memset(dest, c, n);
}

int main(int argc, char **argv)
{
  char *src = calloc(1024, 1024);
  char *dest = calloc(1024, 1024);

  srandom(1539);

  for (int i = 0; i < 16*1024; i++)
    {
      src[i] = (char)random() | 1;
    }

  int count = get_arg(argc, argv, 1, 31);
  int loops = get_arg(argc, argv, 2, 10000000);
  int flush = get_arg(argc, argv, 3, 0);

  src[count] = 0;

  double start = now();

  for (int i = 0; i < loops; i++)
    {
#if defined(WITH_MEMCPY)
      xmemcpy(dest, src, count);
#elif defined(WITH_STRCPY)
      xstrcpy(dest, src);
#elif defined(WITH_MEMSET)
      xmemset(src, 0, count);
#else
#error
#endif

      if (flush != 0)
	{
	  empty(dest);
	}
    }

  double end = now();
  double elapsed = end - start;

  printf("%.3f for %u loops of %u bytes.  %.3f MB/s\n", elapsed, loops, count, (double)loops*count/elapsed/(1024*1024));

  return 0;
}

