// 3D Hero Section - Three.js Globe
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / 2 / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

const container = document.getElementById('hero-canvas');
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// Create Globe
const geometry = new THREE.SphereGeometry(2, 64, 64);
const material = new THREE.MeshPhongMaterial({
    color: 0x2196f3,
    wireframe: true,
    transparent: true,
    opacity: 0.3
});
const globe = new THREE.Mesh(geometry, material);
scene.add(globe);

// Add light
const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

camera.position.z = 5;

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    globe.rotation.y += 0.005;
    renderer.render(scene, camera);
}

// Handle resize
window.addEventListener('resize', () => {
    renderer.setSize(container.clientWidth, container.clientHeight);
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
});

animate();

console.log('NETMARLYN PWA Initialized');
