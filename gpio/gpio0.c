#include <linux/fs.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/module.h>

#include <asm/uaccess.h>

char hello_str = '0';

static ssize_t dev_read(struct file * file, char * buf, 
			  size_t count, loff_t *ppos)
{
	copy_to_user(buf, &hello_str, 1);

	return 1;
}

static ssize_t dev_write(struct file * file, const char * buf, 
			  size_t count, loff_t *ppos)
{
	if(strlen(buf))
	{
		hello_str = buf[strlen(buf) -1];
	}

	return 1;
}

static const struct file_operations dev_fops = {
	.owner		= THIS_MODULE,
	.read		= dev_read,
	.write		= dev_write,
};

static struct miscdevice hello_dev = {

	MISC_DYNAMIC_MINOR,
	"gpio0",
	&dev_fops
};

static int __init
hello_init(void)
{
	int ret;

	ret = misc_register(&hello_dev);
	if (ret)
		printk(KERN_ERR
		       "Unable to register misc device\n");

	return ret;
}

module_init(hello_init);

static void __exit
hello_exit(void)
{
	misc_deregister(&hello_dev);
}

module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("");
MODULE_DESCRIPTION("");
MODULE_VERSION("");
