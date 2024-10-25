from site_setup.models import SiteSetup

def site_setup(requests):
  setup_data = SiteSetup.objects.order_by("-id").first()
  return {
    "site_setup": setup_data
  }
