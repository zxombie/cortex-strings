#include <stddef.h>

void *memset(void *dst0, int c, size_t len0)
{
  char *dst = (char *) dst0;

  void *save = dst0;

  while (len0--)
    {
      *dst++ = c;
    }

  return save;
}
