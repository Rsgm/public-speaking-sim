// Configure the Google Cloud provider
provider "google" {
  credentials = "${file("account.json")}"
  project     = "my-gce-project"
  region      = "us-central1"
}

resource "google_compute_instance_template" "foobar" {
  name           = "foobar"
  machine_type   = "n1-standard-1"
  can_ip_forward = false

  tags = ["foo", "bar"]

  disk {
    source_image = "debian-cloud/debian-7-wheezy-v20160301"
  }

  network_interface {
    network = "default"
  }

  metadata {
    foo = "bar"
  }

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }
}

resource "google_compute_target_pool" "foobar" {
  name = "foobar"
}

resource "google_compute_instance_group_manager" "foobar" {
  name = "foobar"
  zone = "us-central1-f"

  instance_template  = "${google_compute_instance_template.foobar.self_link}"
  target_pools       = ["${google_compute_target_pool.foobar.self_link}"]
  base_instance_name = "foobar"
}

resource "google_compute_autoscaler" "foobar" {
  name   = "foobar"
  zone   = "us-central1-f"
  target = "${google_compute_instance_group_manager.foobar.self_link}"

  autoscaling_policy = {
    max_replicas    = 5
    min_replicas    = 1
    cooldown_period = 60

    cpu_utilization {
      target = 0.5
    }
  }
}
